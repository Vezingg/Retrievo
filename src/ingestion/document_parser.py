import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    """Parser for PDF and web documents."""
    
    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Union[str, int]]]:
        """
        Parse a PDF file and extract text with metadata.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        try:
            doc = fitz.open(file_path)
            chunks = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    chunks.append({
                        "text": text,
                        "source": file_path,
                        "page": page_num + 1,
                        "type": "pdf"
                    })
            
            return chunks
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def parse_webpage(url: str) -> List[Dict[str, Union[str, int]]]:
        """
        Parse a webpage and extract text with metadata.
        
        Args:
            url: URL of the webpage
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Fetched webpage content with status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Log the first 500 characters of the text for debugging
            logger.debug(f"Extracted text preview: {text[:500]}")
            
            # Split into paragraphs
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            
            chunks = []
            for i, para in enumerate(paragraphs):
                if para:
                    chunks.append({
                        "text": para,
                        "source": url,
                        "section": i + 1,
                        "type": "web"
                    })
            
            logger.info(f"Successfully parsed {len(chunks)} sections from the webpage.")
            return chunks
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request error for {url}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error parsing webpage {url}: {str(e)}")
            return []
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and normalizing.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()