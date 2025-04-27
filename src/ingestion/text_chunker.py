from typing import List, Dict, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextChunker:
    """Handles splitting text into chunks for embedding."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_document(self, document: Dict[str, Union[str, int]]) -> List[Dict[str, Union[str, int]]]:
        """
        Split a document into chunks while preserving metadata.
        
        Args:
            document: Dictionary containing text and metadata
            
        Returns:
            List of chunked documents with preserved metadata
        """
        try:
            # Split the text into chunks
            chunks = self.text_splitter.split_text(document["text"])
            
            # Create new documents with the same metadata but chunked text
            chunked_docs = []
            for i, chunk in enumerate(chunks):
                chunked_doc = document.copy()
                chunked_doc["text"] = chunk
                chunked_doc["chunk_id"] = i + 1
                chunked_docs.append(chunked_doc)
            
            return chunked_docs
        except Exception as e:
            logger.error(f"Error chunking document: {str(e)}")
            return []
    
    def chunk_documents(self, documents: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
        """
        Split multiple documents into chunks.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of all chunked documents
        """
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        return all_chunks 