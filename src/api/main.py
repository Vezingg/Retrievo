from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Union
import os
import logging
from ..ingestion import IngestionPipeline
from src.agent.react_agent import ReActAgent
from src.generation.llm import LLMGenerator
from src.retrieval.vector_store import VectorStore
from src.ingestion.embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Pipeline API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
ingestion_pipeline = IngestionPipeline()
vector_store = ingestion_pipeline.vector_store  # Use the vector store from the pipeline
embedder = EmbeddingGenerator()
llm_generator = LLMGenerator()
agent = ReActAgent(vector_store, embedder, llm_generator)

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    """
    try:
        # Save the uploaded file
        file_path = f"data/uploads/{file.filename}"
        os.makedirs("data/uploads", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process the PDF
        ingestion_pipeline.process_pdf(file_path)
        
        return {"message": f"Successfully processed {file.filename}"}
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/url")
async def process_url(url: str):
    """
    Process a webpage URL.
    """
    try:
        ingestion_pipeline.process_webpage(url)
        return {"message": f"Successfully processed {url}"}
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def process_query(query: str):
    """
    Process a user query using the ReAct agent.
    """
    try:
        response = agent.process_query(query)
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz/check")
async def check_answer(question: str, user_answer: str, correct_answer: str):
    """
    Check a user's answer to a quiz question.
    """
    try:
        feedback = agent.check_answer(question, user_answer, correct_answer)
        return feedback
    except Exception as e:
        logger.error(f"Error checking answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Reverted port back to 8000

# uvicorn src.api.main:app --host 0.0.0.0 --port 8000