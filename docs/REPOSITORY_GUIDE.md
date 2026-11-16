# Chatbot/RAG Repository Guide

This repository is the S4 local RAG chatbot prototype for Dobot MG400 learning
and project support. It contains the Streamlit application, preprocessing and
ingest scripts, prompts, curated cards, and evaluation summaries.

The large source corpus and ChromaDB runtime snapshot are intentionally omitted
from this GitHub preparation copy. Rebuild the index from an approved corpus on
the target machine rather than committing generated vector databases.

## Main flow

```text
approved documents -> preprocess -> chunks -> embeddings -> ChromaDB
question -> retrieval/reranking -> Ollama -> answer with citations
```

The chatbot is an information assistant. The checked application code does not
contain a direct Dobot motion interface. Any future handoff to ARC must define a
separate contract, validation, approval, and stop/recovery path.

## Main files

- `chatbot/app/rag.py`: retrieval, reranking, context assembly, generation, and fallback.
- `chatbot/app/streamlit_app.py`: Streamlit UI and retrieved-source display.
- `chatbot/config/settings.py`: environment-backed defaults.
- `chatbot/scripts/preprocess.py`: corpus selection and chunk generation.
- `chatbot/scripts/ingest.py`: embedding and ChromaDB ingestion.
- `chatbot/prompts/system_prompt.txt`: answer and safety guidance.

## Status

This is a confirmed local RAG prototype. Active model, collection, corpus
licensing, human factual review, learning outcomes, and ARC mapping remain
**To Verify**.
