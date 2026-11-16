# Chatbot Data Directory

The committed data in this directory is limited to small curated cards,
manifests, and evaluation summaries. Generated ChromaDB files and derived
corpus text are excluded from the GitHub preparation snapshot.

To recreate a local index, provide an approved corpus, configure the embedding
and Ollama models in `.env`, then run the preprocessing and ingest scripts from
the `chatbot/` directory. Do not commit credentials, model caches, or the
resulting database.
