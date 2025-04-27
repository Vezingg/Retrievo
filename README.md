# RAG Pipeline for Q&A, Summarization & Quizzes

A Retrieval-Augmented Generation (RAG) pipeline that can ingest external documents (PDFs and web pages) and use them to power an intelligent Q&A and study assistant.

## Features

- Document ingestion from PDFs and websites
- Semantic search using FAISS vector store
- Q&A with source citations
- Document summarization
- Quiz generation and answer checking
- ReAct agent with tools for complex queries

## Setup

### Option 1: Using Conda (Recommended)

1. Install [Conda](https://docs.conda.io/en/latest/miniconda.html) if you don't have it already.

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate rag-pipeline
```

3. Set up environment variables:
Create a `.env` file with:
```
MISTRAL_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

### Option 2: Using pip

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
MISTRAL_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python main.py
```

## Project Structure

- `src/` - Source code
  - `ingestion/` - Document parsing and embedding
  - `retrieval/` - Vector store and search
  - `generation/` - LLM integration
  - `agent/` - ReAct agent and tools
  - `api/` - FastAPI endpoints
  - `ui/` - Streamlit interface

## Usage

1. Upload documents (PDFs or URLs)
2. Ask questions about the content
3. Request summaries
4. Generate and take quizzes

## Development

The project uses:
- Python 3.10+
- Mistral AI for embeddings and LLM
- FAISS for vector storage
- LangChain for orchestration
- FastAPI for backend
- Streamlit for frontend

## Troubleshooting

If you encounter any issues with the conda environment:

1. Make sure you have the latest conda:
```bash
conda update conda
```

2. If you need to update the environment:
```bash
conda env update -f environment.yml
```

3. If you need to remove and recreate the environment:
```bash
conda deactivate
conda env remove -n rag-pipeline
conda env create -f environment.yml
``` 