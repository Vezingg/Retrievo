from typing import List, Dict, Union, Tuple
import faiss
import numpy as np
import logging
import pickle
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """FAISS-based vector store for document retrieval."""
    
    def __init__(self, dimension: int = 1024):
        """
        Initialize the vector store.
        
        Args:
            dimension: Dimension of the embedding vectors
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.documents = []  # Store document metadata and text
        logger.info(f"Initialized vector store with dimension {dimension}")
    
    def add_documents(self, documents: List[Dict[str, Union[str, int, np.ndarray]]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document dictionaries with embeddings
        """
        try:
            if not documents:
                logger.warning("No documents provided to add to vector store")
                return
                
            # Validate embeddings
            for doc in documents:
                if "embedding" not in doc:
                    logger.error("Document missing embedding")
                    return
                if not isinstance(doc["embedding"], np.ndarray):
                    logger.error("Document embedding is not a numpy array")
                    return
                if doc["embedding"].shape[0] != self.dimension:
                    logger.error(f"Document embedding dimension {doc['embedding'].shape[0]} does not match vector store dimension {self.dimension}")
                    return
            
            # Extract embeddings
            embeddings = np.array([doc["embedding"] for doc in documents])
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store documents
            self.documents.extend(documents)
            
            logger.info(f"Added {len(documents)} documents to vector store. Total documents: {len(self.documents)}")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        try:
            # Check if index is empty
            if self.index.ntotal == 0:
                logger.warning("Vector store index is empty. No documents have been added.")
                return []
            
            # Search in FAISS
            scores, indices = self.index.search(query_embedding.reshape(1, -1), k)
            
            # Get documents and scores
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents):
                    results.append((self.documents[idx], float(score)))
            
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    def save(self, directory: str) -> None:
        """
        Save the vector store to disk.
        
        Args:
            directory: Directory to save the files
        """
        try:
            # Convert to absolute path
            directory = os.path.abspath(directory)
            os.makedirs(directory, exist_ok=True)
            
            # Save FAISS index
            index_path = os.path.join(directory, "index.faiss")
            faiss.write_index(self.index, index_path)
            
            # Save documents
            documents_path = os.path.join(directory, "documents.pkl")
            with open(documents_path, "wb") as f:
                pickle.dump(self.documents, f)
            
            logger.info(f"Saved vector store to {directory}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
    
    def load(self, directory: str) -> None:
        """
        Load the vector store from disk.
        
        Args:
            directory: Directory containing the saved files
        """
        try:
            # Convert to absolute path
            directory = os.path.abspath(directory)
            
            # Check if directory exists
            if not os.path.exists(directory):
                logger.error(f"Vector store directory does not exist: {directory}")
                return
                
            # Check if files exist
            index_path = os.path.join(directory, "index.faiss")
            documents_path = os.path.join(directory, "documents.pkl")
            
            if not os.path.exists(index_path):
                logger.error(f"FAISS index file does not exist: {index_path}")
                return
                
            if not os.path.exists(documents_path):
                logger.error(f"Documents file does not exist: {documents_path}")
                return
            
            # Load FAISS index
            self.index = faiss.read_index(index_path)
            
            # Load documents
            with open(documents_path, "rb") as f:
                self.documents = pickle.load(f)
            
            logger.info(f"Loaded vector store from {directory}")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}") 