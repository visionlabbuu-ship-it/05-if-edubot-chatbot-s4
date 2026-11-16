"""Streamlit UI for Dobot MG400 RAG chatbot."""
from __future__ import annotations

import sys
from pathlib import Path

# chatbot/ on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from app.rag import RagEngine
from config import settings

st.set_page_config(
    page_title="Dobot MG400 Assistant",
    page_icon="🤖",
    layout="wide",
)

SAMPLE_QUESTIONS = [
    "MG400 payload และ working radius เท่าไร?",
    "MG400 ใช้ TCP/IP port อะไรบ้าง?",
    "TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม?",
    "ช่วยเขียน Python skeleton เชื่อม MG400 แบบยังไม่สั่ง motion",
    "ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง?",
    "ถ้าเชื่อมต่อ TCP/IP ไม่ได้ควรตรวจอะไร?",
    "What is MG400?",
    "Explain EnableRobot and DisableRobot from the API docs.",
]


@st.cache_resource(show_spinner="Loading RAG engine / embedding model...")
def get_engine() -> RagEngine:
    return RagEngine()


def _resolve_installed_name(tag: str, installed: list[str]) -> str | None:
    """Map a recommended tag to an actual installed Ollama name."""
    if tag in installed:
        return tag
    if f"{tag}:latest" in installed:
        return f"{tag}:latest"
    for m in installed:
        if m == tag or m.startswith(tag + ":"):
            return m
        # allow recommending "llama3.2" when installed is "llama3.2:latest"
        base = m[:-7] if m.endswith(":latest") else m
        if base == tag:
            return m
    return None


def _model_options(engine: RagEngine) -> list[str]:
    """Recommended models first, then other installed Ollama tags."""
    installed = engine.list_ollama_models()
    resolved: list[str] = []
    for rec in settings.OLLAMA_RECOMMENDED_MODELS:
        name = _resolve_installed_name(rec, installed)
        if name and name not in resolved:
            resolved.append(name)
    for m in installed:
        if m not in resolved:
            resolved.append(m)
    if not resolved:
        resolved = [settings.OLLAMA_MODEL]
    return resolved


def main() -> None:
    st.title("🤖 Dobot MG400 Learning Assistant")
    st.caption(
        "Local RAG chatbot · tight corpus (manuals, Studio, TCP/IP, Python, demos, scrubbed FAQ)"
    )

    engine = get_engine()

    with st.sidebar:
        st.header("สถานะระบบ")
        try:
            n_chunks = engine.chunk_count
        except Exception as exc:  # noqa: BLE001
            st.error(f"Chroma index error: {exc}")
            if st.button("Reload RAG engine", type="primary"):
                get_engine.clear()
                st.rerun()
            st.stop()

        st.write(f"**Chunks in index:** {n_chunks}")
        st.write(f"**Collection:** `{settings.COLLECTION_NAME}`")
        st.write(f"**Embedding:** `{settings.EMBEDDING_MODEL}`")

        st.divider()
        st.subheader("LLM model")
        options = _model_options(engine)
        default_model = settings.OLLAMA_MODEL
        if "ollama_model" not in st.session_state:
            pick = _resolve_installed_name(default_model, options) or options[0]
            st.session_state.ollama_model = pick

        # Keep selectbox index valid if models list changed
        current = st.session_state.ollama_model
        if current not in options:
            st.session_state.ollama_model = options[0]

        selected_model = st.selectbox(
            "เลือกโมเดล Ollama",
            options=options,
            help="เปลี่ยนได้ทันที — ไม่ต้อง restart (ต้อง pull โมเดลใน Ollama ก่อน)",
            key="ollama_model",
        )

        labels = {
            "qwen3.5:9b": "⚡ แนะนำ · เร็ว · รุ่นใหม่",
            "qwen3:14b": "🎯 คุณภาพ · ช้ากว่าเล็กน้อย",
            "llama3.2": "🪶 เบา · คุณภาพต่ำกว่า",
        }
        for tag, note in labels.items():
            if selected_model == tag or selected_model.startswith(tag):
                st.caption(note)
                break

        ok, msg = engine.ollama_available(selected_model)
        if ok:
            st.success(f"Ollama: {msg}")
        else:
            st.warning(f"Ollama: {msg}")
            st.info(
                "ถ้ายังไม่มี LLM ระบบจะตอบแบบ extractive จากเอกสาร "
                "(แสดง snippet + citation) แทน\n\n"
                f"ติดตั้ง: `ollama pull {selected_model}`"
            )

        think = st.checkbox(
            "Qwen thinking mode",
            value=settings.OLLAMA_THINK,
            help="เปิดเฉพาะตอนต้องการเหตุผลยาว — RAG ปกติควรปิดเพื่อความเร็ว",
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=float(settings.OLLAMA_TEMPERATURE),
            step=0.05,
        )

        st.divider()
        top_k = st.slider("Top-K retrieval", 3, 12, settings.TOP_K)
        show_context = st.checkbox("แสดง retrieved chunks", value=True)
        if st.button("Reload RAG engine", help="ใช้หลัง ingest --reset ถ้า index เปลี่ยน"):
            get_engine.clear()
            st.rerun()
        st.divider()
        st.markdown("**คำถามตัวอย่าง**")
        for q in SAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True):
                st.session_state["pending_question"] = q

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("model"):
                st.caption(f"model: `{msg['model']}`")
            if msg.get("chunks") and show_context:
                with st.expander("Retrieved sources"):
                    for ch in msg["chunks"]:
                        st.markdown(
                            f"**{ch['citation']}**  \nscore/distance: `{ch.get('distance')}`"
                        )
                        st.code(ch["text"][:800])

    prompt = st.chat_input("ถามเกี่ยวกับ MG400, API, safety, โครงงาน...")
    if "pending_question" in st.session_state:
        prompt = st.session_state.pop("pending_question")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"กำลังค้นเอกสาร + สร้างคำตอบด้วย `{selected_model}`..."):
                result = engine.ask(
                    prompt,
                    top_k=top_k,
                    model=selected_model,
                    temperature=temperature,
                    think=think,
                )
            st.markdown(result["answer"])
            st.caption(f"model: `{result.get('model', selected_model)}`")
            if show_context and result["chunks"]:
                with st.expander("Retrieved sources"):
                    for ch in result["chunks"]:
                        st.markdown(
                            f"**{ch['citation']}**  \nscore/distance: `{ch.get('distance')}`"
                        )
                        st.code(ch["text"][:800])

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "model": result.get("model", selected_model),
                "chunks": result["chunks"],
            }
        )

    if n_chunks == 0:
        st.error(
            "Knowledge Base ว่าง — รัน preprocess + ingest ก่อน:\n\n"
            "```\ncd chatbot\npython scripts/preprocess.py\npython scripts/ingest.py --reset\n```"
        )


if __name__ == "__main__":
    main()
