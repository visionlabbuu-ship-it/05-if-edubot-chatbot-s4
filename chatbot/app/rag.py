"""Retrieval + generation for Dobot MG400 chatbot."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import chromadb
import httpx
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import settings


@dataclass
class RetrievedChunk:
    id: str
    text: str
    distance: float | None
    metadata: dict[str, Any]

    @property
    def citation(self) -> str:
        title = self.metadata.get("doc_title") or self.metadata.get("source_path") or self.id
        page = self.metadata.get("page") or ""
        section = self.metadata.get("section") or ""
        parts = [str(title)]
        if page:
            parts.append(f"p.{page}")
        if section and section not in {"body", "faq"}:
            parts.append(section)
        return " | ".join(parts)


def _query_intents(query: str) -> set[str]:
    q = query.lower()
    intents: set[str] = set()
    if re.search(r"port|29999|30003|30004|dashboard|feedback|lan1|lan2|modbus|502|tcp", q):
        intents.add("ports")
    if re.search(r"tcp/?ip|4-?\s*axis|remote control|interface guide", q):
        intents.add("api_guide")
    if re.search(r"payload|reach|radius|spec|น้ำหนัก|ระยะ|สเปก|repeatab", q):
        intents.add("specs")
    if re.search(r"safety|ปลอดภัย|movj|movl|enable|ก่อนสั่ง|e-?stop|collision|checklist", q):
        intents.add("safety")
    if re.search(r"python|dobot_api|skeleton|sdk|code|สคริปต์|โค้ด|connect|เชื่อม", q):
        intents.add("code")
    if re.search(r"studio|dobotstudio|crstudio|blockly|teach|โปรแกรม", q):
        intents.add("software")
    if re.search(r"pallet|conveyor|vision|sorting|demo|โครงงาน|training", q):
        intents.add("demo")
    if re.search(r"alarm|error|fault|รหัสผิด|error.?id|servo.?alarm", q):
        intents.add("alarm")
    if re.search(r"ros|service\.srv|topic", q):
        intents.add("ros")
    return intents


def _rerank_score(chunk: RetrievedChunk, intents: set[str]) -> float:
    """Lower is better (compatible with cosine distance)."""
    base = float(chunk.distance if chunk.distance is not None else 1.0)
    dt = (chunk.metadata.get("doc_type") or "").lower()
    title = (chunk.metadata.get("doc_title") or "").lower()
    prio = (chunk.metadata.get("priority") or "").lower()
    boost = 0.0  # subtracted from distance

    if dt == "cheat_sheet":
        boost += 0.12
    if prio == "high":
        boost += 0.02

    if "ports" in intents:
        if dt in {"cheat_sheet", "api_reference", "faq"} or "port" in title:
            boost += 0.14
        if "29999" in chunk.text or "30003" in chunk.text or "30004" in chunk.text:
            boost += 0.08
    if "api_guide" in intents:
        if dt == "api_reference" or "tcp/ip remote" in title or "4-axis" in title:
            boost += 0.16
        if dt == "sdk_code" and "readme" in title:
            boost += 0.08
    if "specs" in intents:
        if dt in {"datasheet", "manual", "cheat_sheet", "faq"} or "spec" in title:
            boost += 0.10
    if "safety" in intents:
        if dt in {"cheat_sheet", "manual"} or "safety" in title:
            boost += 0.14
    if "code" in intents:
        if dt in {"cheat_sheet", "sdk_code", "api_reference"} or "python" in title:
            boost += 0.12
        if dt in {"case_study", "demo_guide"}:
            boost -= 0.04
    if "software" in intents:
        if dt == "software_manual" or "studio" in title:
            boost += 0.16
    if "demo" in intents:
        if dt in {"demo_guide", "demo_script", "case_study"}:
            boost += 0.12
    if "alarm" in intents:
        if dt == "error_code":
            boost += 0.15
    else:
        # Alarms dominate the index; demote unless asked
        if dt == "error_code":
            boost -= 0.10
    if "ros" in intents:
        if dt == "ros_api" or "ros" in title:
            boost += 0.12

    return base - boost


class RagEngine:
    def __init__(self) -> None:
        self._ef = SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL,
        )
        self._client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
        self._collection = self._bind_collection()
        self._system_prompt_path = settings.SAFETY_PROMPT_PATH
        self._system_prompt = self._system_prompt_path.read_text(encoding="utf-8")

    def _bind_collection(self):
        """Open (or create) the configured Chroma collection by name."""
        return self._client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )

    def _ensure_collection(self):
        """
        Rebind if the cached collection handle is stale.

        After ingest --reset, Chroma may recreate the same name with a new UUID.
        Streamlit's @st.cache_resource can keep an old RagEngine that still points
        at the deleted collection id → NotFoundError on count/query.
        """
        try:
            self._collection.count()
            return self._collection
        except Exception as exc:  # noqa: BLE001
            name = type(exc).__name__
            msg = str(exc).lower()
            if name == "NotFoundError" or "does not exist" in msg:
                # Also recreate client in case the on-disk store was rewritten
                self._client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
                self._collection = self._bind_collection()
                return self._collection
            raise

    def reload_system_prompt(self) -> None:
        """Re-read system prompt from disk (useful after edits without restarting)."""
        self._system_prompt = self._system_prompt_path.read_text(encoding="utf-8")

    @property
    def chunk_count(self) -> int:
        return self._ensure_collection().count()

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        k = top_k or settings.TOP_K
        collection = self._ensure_collection()
        n = collection.count()
        if n == 0:
            return []
        # Over-fetch then intent-rerank (full corpus is noisy without this)
        fetch_k = min(max(k * 5, 24), n)
        result = collection.query(
            query_texts=[query],
            n_results=fetch_k,
            include=["documents", "metadatas", "distances"],
        )
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        ids = (result.get("ids") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        out: list[RetrievedChunk] = []
        for i, doc in enumerate(docs):
            out.append(
                RetrievedChunk(
                    id=ids[i],
                    text=doc or "",
                    distance=dists[i] if i < len(dists) else None,
                    metadata=metas[i] or {},
                )
            )
        intents = _query_intents(query)
        out.sort(key=lambda c: _rerank_score(c, intents))
        # Deduplicate near-identical titles keeping best score
        seen_titles: set[str] = set()
        deduped: list[RetrievedChunk] = []
        for ch in out:
            key = f"{ch.metadata.get('doc_title')}|{ch.metadata.get('page')}|{(ch.text or '')[:80]}"
            if key in seen_titles:
                continue
            seen_titles.add(key)
            deduped.append(ch)
            if len(deduped) >= k:
                break
        return deduped

    def build_context(self, chunks: list[RetrievedChunk]) -> str:
        blocks = []
        for i, ch in enumerate(chunks, start=1):
            blocks.append(
                f"[Source {i}] {ch.citation}\n{ch.text}"
            )
        return "\n\n---\n\n".join(blocks)

    def list_ollama_models(self) -> list[str]:
        """Return installed Ollama model names (empty if unreachable)."""
        try:
            r = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            r.raise_for_status()
            names = [m.get("name", "") for m in r.json().get("models", []) if m.get("name")]
            return sorted(set(names))
        except Exception:  # noqa: BLE001
            return []

    @staticmethod
    def _model_matches(installed: str, wanted: str) -> bool:
        """Match exact tag or common prefix forms (qwen3:14b vs qwen3:14b:latest)."""
        if not wanted:
            return False
        if installed == wanted:
            return True
        if installed.startswith(wanted + ":") or wanted.startswith(installed + ":"):
            return True
        # strip :latest
        def _base(name: str) -> str:
            return name[:-7] if name.endswith(":latest") else name

        return _base(installed) == _base(wanted)

    def ollama_available(self, model: str | None = None) -> tuple[bool, str]:
        try:
            r = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            r.raise_for_status()
            models = [m.get("name", "") for m in r.json().get("models", []) if m.get("name")]
            if not models:
                return False, "Ollama is running but no models are installed."
            wanted = model or settings.OLLAMA_MODEL
            if any(self._model_matches(m, wanted) for m in models):
                return True, f"OK · using `{wanted}` ({len(models)} models installed)"
            return False, f"Model '{wanted}' not found. Installed: {', '.join(models)}"
        except Exception as exc:  # noqa: BLE001
            return False, f"Ollama not reachable: {exc}"

    def generate(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        *,
        model: str | None = None,
        temperature: float | None = None,
        think: bool | None = None,
    ) -> str:
        if not chunks:
            return (
                "ไม่พบข้อมูลใน Knowledge Base ที่โหลดไว้\n\n"
                "No retrieved context. Please run preprocess + ingest first, "
                "or rephrase the question about MG400 manuals/API/FAQ."
            )

        # Pick up prompt edits without full process restart
        try:
            self.reload_system_prompt()
        except Exception:  # noqa: BLE001
            pass

        context = self.build_context(chunks)
        user_prompt = (
            f"Retrieved context:\n{context}\n\n"
            f"User question:\n{question}\n\n"
            "Instructions for this answer:\n"
            "- Use facts from the retrieved context above. Do not invent numbers or ports.\n"
            "- If the context already answers the question (including synonyms), "
            "state the answer directly. Do NOT start with 'ไม่พบข้อมูล' / 'not found'.\n"
            "- If a safety checklist or port table is present, turn it into clear bullets.\n"
            "- Start with the direct answer, then brief steps/notes, then Sources.\n"
            "- Same language as the user question.\n"
        )

        llm_model = (model or settings.OLLAMA_MODEL).strip()
        ok, msg = self.ollama_available(llm_model)
        if not ok:
            return self._fallback_extractive(question, chunks, reason=msg)

        temp = settings.OLLAMA_TEMPERATURE if temperature is None else float(temperature)
        use_think = settings.OLLAMA_THINK if think is None else bool(think)

        payload: dict[str, Any] = {
            "model": llm_model,
            "stream": False,
            "options": {
                "temperature": temp,
                # Room for retrieved chunks + answer on 9B/14B
                "num_ctx": 16384,
            },
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        # Qwen3 / Qwen3.5 support think flag (false = faster grounded answers)
        model_l = llm_model.lower()
        if "qwen3" in model_l or "qwen3.5" in model_l:
            payload["think"] = use_think
        try:
            r = httpx.post(
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=settings.OLLAMA_TIMEOUT,
            )
            r.raise_for_status()
            data = r.json()
            content = (data.get("message") or {}).get("content") or data.get("response") or ""
            if not content.strip():
                return self._fallback_extractive(question, chunks, reason="Empty LLM response")
            return content.strip()
        except Exception as exc:  # noqa: BLE001
            return self._fallback_extractive(question, chunks, reason=str(exc))

    def _fallback_extractive(
        self, question: str, chunks: list[RetrievedChunk], reason: str
    ) -> str:
        """If LLM is unavailable, return top snippets with citations (still useful)."""
        lines = [
            "### คำตอบแบบ Extractive (LLM ยังไม่พร้อม)",
            f"_เหตุผล: {reason}_",
            "",
            f"**คำถาม:** {question}",
            "",
            "จากเอกสารที่เกี่ยวข้องที่สุด:",
            "",
        ]
        for i, ch in enumerate(chunks[:4], start=1):
            snippet = ch.text.strip().replace("\n", " ")
            if len(snippet) > 500:
                snippet = snippet[:500] + "..."
            lines.append(f"**{i}. {ch.citation}**")
            lines.append(snippet)
            lines.append("")
        lines.append("Sources:")
        for ch in chunks[:4]:
            lines.append(f"- {ch.citation}")
        lines.append("")
        lines.append(
            "หมายเหตุ: เมื่อ Ollama พร้อม ระบบจะสรุปคำตอบให้อ่านง่ายขึ้นอัตโนมัติ"
        )
        return "\n".join(lines)

    def ask(
        self,
        question: str,
        top_k: int | None = None,
        *,
        model: str | None = None,
        temperature: float | None = None,
        think: bool | None = None,
    ) -> dict[str, Any]:
        llm_model = (model or settings.OLLAMA_MODEL).strip()
        chunks = self.retrieve(question, top_k=top_k)
        answer = self.generate(
            question,
            chunks,
            model=llm_model,
            temperature=temperature,
            think=think,
        )
        return {
            "answer": answer,
            "model": llm_model,
            "chunks": [
                {
                    "id": c.id,
                    "citation": c.citation,
                    "distance": c.distance,
                    "metadata": c.metadata,
                    "text": c.text,
                }
                for c in chunks
            ],
        }
