from typing import List, Dict, Union
import os
import logging
from .document_parser import DocumentParser
from .text_chunker import TextChunker
from .embedding_generator import EmbeddingGenerator
from ..retrieval.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionPipeline:
    """Main pipeline for document ingestion and indexing."""
    
    def __init__(self, vector_store_dir: str = "data/vector_store"):
        """
        Initialize the ingestion pipeline.
        
        Args:
            vector_store_dir: Directory to store the vector store
        """
        self.parser = DocumentParser()
        self.chunker = TextChunker()
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.vector_store_dir = os.path.abspath(vector_store_dir)
        
        # Create vector store directory if it doesn't exist
        os.makedirs(self.vector_store_dir, exist_ok=True)
        
        # Try to load existing vector store
        try:
            self.vector_store.load(self.vector_store_dir)
            logger.info("Loaded existing vector store")
        except Exception as e:
            logger.warning(f"Could not load existing vector store: {str(e)}")
    
    def process_pdf(self, file_path: str) -> None:
        """
        Process a PDF file through the pipeline.
        
        Args:
            file_path: Path to the PDF file
        """
        try:
            # Parse PDF
            logger.info(f"Parsing PDF: {file_path}")
            documents = self.parser.parse_pdf(file_path)
            if not documents:
                logger.error(f"No documents extracted from PDF: {file_path}")
                return
            logger.info(f"Extracted {len(documents)} documents from PDF")
            
            # Clean text
            for doc in documents:
                doc["text"] = self.parser.clean_text(doc["text"])
            
            # Chunk documents
            logger.info("Chunking documents")
            chunked_docs = self.chunker.chunk_documents(documents)
            if not chunked_docs:
                logger.error("No chunks generated from documents")
                return
            logger.info(f"Generated {len(chunked_docs)} chunks")
            
            # Generate embeddings
            logger.info("Generating embeddings")
            embedded_docs = self.embedder.embed_documents(chunked_docs)
            if not embedded_docs:
                logger.error("No embeddings generated")
                return
            logger.info(f"Generated embeddings for {len(embedded_docs)} chunks")
            
            # Add to vector store
            logger.info("Adding to vector store")
            self.vector_store.add_documents(embedded_docs)
            
            # Save vector store
            self.vector_store.save(self.vector_store_dir)
            
            logger.info(f"Successfully processed PDF: {file_path}")
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
    
    def process_webpage(self, url: str) -> None:
        """
        Process a webpage through the pipeline.
        
        Args:
            url: URL of the webpage
        """
        try:
            # Parse webpage
            logger.info(f"Parsing webpage: {url}")
            documents = self.parser.parse_webpage(url)
            
            # Clean text
            for doc in documents:
                doc["text"] = self.parser.clean_text(doc["text"])
            
            # Chunk documents
            logger.info("Chunking documents")
            chunked_docs = self.chunker.chunk_documents(documents)
            
            # Generate embeddings
            logger.info("Generating embeddings")
            embedded_docs = self.embedder.embed_documents(chunked_docs)
            
            # Add to vector store
            logger.info("Adding to vector store")
            self.vector_store.add_documents(embedded_docs)
            
            # Save vector store
            self.vector_store.save(self.vector_store_dir)
            
            logger.info(f"Successfully processed webpage: {url}")
        except Exception as e:
            logger.error(f"Error processing webpage {url}: {str(e)}")
    
    def load_existing_vector_store(self) -> None:
        """Load the existing vector store from disk."""
        try:
            self.vector_store.load(self.vector_store_dir)
            logger.info("Loaded existing vector store")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}") 