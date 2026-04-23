# RAG-Based Customer Support Assistant

This is a Retrieval-Augmented Generation (RAG) based customer support assistant built with Python, LangChain, HuggingFace Transformers, and ChromaDB.

## Features

- Loads customer support documents from a knowledge base
- Splits documents into chunks and creates embeddings using HuggingFace models
- Stores embeddings in a vector database (ChromaDB)
- Provides a query interface to answer customer questions using retrieved relevant information and a local LLM (GPT-2)

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Build the vector store (this will download the embedding model on first run):
   ```
   python scripts/build_vector_store.py
   ```

3. Run the application (this will download the language model on first run):
   ```
   streamlit run src/app.py
   ```

Note: The first run may take time to download the required models (~1GB total).

## Architecture

- **Data Layer**: Knowledge base documents in `data/`
- **Vector Store**: ChromaDB for storing document embeddings
- **Embeddings**: HuggingFace sentence-transformers for creating embeddings
- **Retrieval**: LangChain for retrieving relevant documents
- **Generation**: HuggingFace GPT-2 for generating answers based on retrieved context
- **Interface**: Streamlit for user interaction

## Workflow

1. Documents are loaded and split into chunks.
2. Embeddings are created using HuggingFace sentence-transformers.
3. Chunks are stored in ChromaDB vector store.
4. User query is embedded and similar documents are retrieved.
5. Retrieved documents are passed to GPT-2 LLM with the query to generate an answer.