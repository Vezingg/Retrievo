from typing import List, Dict, Union
import litellm
from litellm import embedding
import os
from dotenv import load_dotenv
import logging
import numpy as np

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generates embeddings for text using Mistral's embedding model with automatic batch splitting."""

    def __init__(self):
        """Initialize the embedding generator and batch settings."""
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        litellm.api_key = self.api_key
        # maximum number of texts per initial batch
        self.batch_size = int(os.getenv("EMBED_BATCH_SIZE", 50))

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        """
        try:
            resp = embedding(
                model="mistral/mistral-embed",
                input=[text],
            )
            return np.array(resp["data"][0]["embedding"])
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(1024)

    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts in batch, recursively splitting on token errors.
        """
        def process_batch(batch_texts: List[str]) -> List[np.ndarray]:
            try:
                resp = embedding(
                    model="mistral/mistral-embed",
                    input=batch_texts,
                )
                return [np.array(item["embedding"]) for item in resp["data"]]
            except litellm.BadRequestError as e:
                # split into smaller batches if too many tokens
                if len(batch_texts) > 1:
                    mid = len(batch_texts) // 2
                    return process_batch(batch_texts[:mid]) + process_batch(batch_texts[mid:])
                else:
                    logger.error(f"Single text too large to embed, returning zeros: {batch_texts[0][:50]}...")
                    return [np.zeros(1024)]
            except Exception as e:
                logger.error(f"Unexpected error in batch embedding: {e}")
                return [np.zeros(1024) for _ in batch_texts]

        embeddings: List[np.ndarray] = []
        # initial slicing into manageable chunks
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            embeddings.extend(process_batch(batch))
        return embeddings

    def embed_documents(self, documents: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int, np.ndarray]]]:
        """
        Embed a list of documents and attach embedding vectors.
        """
        try:
            texts = [doc["text"] for doc in documents]
            embeddings = self.generate_embeddings_batch(texts)
            for doc, emb in zip(documents, embeddings):
                doc["embedding"] = emb
            return documents
        except Exception as e:
            logger.error(f"Error embedding documents: {e}")
            return documents
