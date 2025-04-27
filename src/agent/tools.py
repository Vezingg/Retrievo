from typing import List, Dict, Union, Tuple
import logging
from ..retrieval.vector_store import VectorStore
from ..generation.llm import LLMGenerator
from ..ingestion.embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentSearchTool:
    """Tool for searching documents in the vector store."""
    
    def __init__(self, vector_store: VectorStore, embedder: EmbeddingGenerator):
        """
        Initialize the document search tool.
        
        Args:
            vector_store: Vector store instance
            embedder: Embedding generator instance
        """
        self.vector_store = vector_store
        self.embedder = embedder
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        try:
            # Generate query embedding
            query_embedding = self.embedder.generate_embedding(query)
            
            # Search vector store
            results = self.vector_store.search(query_embedding, k=k)
            
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []

class SummarizationTool:
    """Tool for summarizing documents."""
    
    def __init__(self, llm_generator: LLMGenerator):
        """
        Initialize the summarization tool.
        
        Args:
            llm_generator: LLM generator instance
        """
        self.llm_generator = llm_generator
    
    def summarize(self, text: str) -> str:
        """
        Generate a summary of the text.
        
        Args:
            text: Text to summarize
            
        Returns:
            Generated summary
        """
        try:
            return self.llm_generator.summarize_text(text)
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return "Error generating summary."

class QuizGenerationTool:
    """Tool for generating quiz questions."""
    
    def __init__(self, llm_generator: LLMGenerator):
        """
        Initialize the quiz generation tool.
        
        Args:
            llm_generator: LLM generator instance
        """
        self.llm_generator = llm_generator
    
    def generate_quiz(self, text: str) -> List[Dict[str, str]]:
        """
        Generate quiz questions from the text.
        
        Args:
            text: Text to generate quiz from
            
        Returns:
            List of dictionaries containing questions and answers
        """
        try:
            return self.llm_generator.generate_quiz(text)
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            return [] 