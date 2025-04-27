from typing import List, Dict
import os
from dotenv import load_dotenv
import logging
import litellm
from litellm import completion
from langchain.prompts import PromptTemplate
from langchain_community.chat_models.litellm import ChatLiteLLM  # requires langchain-community & langchain-litellm

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMGenerator:
    """Handles text generation using Mistral's LLM via LiteLLM chat API and provides an LLM interface for agents."""
    def __init__(self):
        """Initialize the LLM generator, chat model, and templates."""
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        litellm.api_key = self.api_key
        self.model_name = "mistral-small-latest"

        # Initialize ChatLiteLLM for agent use, specifying provider
        self.llm = ChatLiteLLM(
            model=self.model_name,
            custom_llm_provider="mistral"
        )

        # Prompt templates for manual calls
        self.qa_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
Use the following context to answer the question. If the context does not have the answer, say you don't know. Give the answer in a few sentences and include a citation to the source.

Context:
{context}

Question: {question}

Answer:"""
        )
        self.summary_template = PromptTemplate(
            input_variables=["text"],
            template="""
Summarize the following text in a concise way, capturing the main points:

{text}

Summary:"""
        )
        self.quiz_template = PromptTemplate(
            input_variables=["text"],
            template="""
Generate 5 quiz questions based on the following content. The questions should be open-ended and test understanding. Provide the correct answer after each question.

Content:
{text}

Questions and Answers:"""
        )

    def answer_question(self, context: str, question: str) -> str:
        """Generate an answer to a question based on context using chat completion."""
        prompt = self.qa_template.format(context=context, question=question)
        try:
            resp = completion(
                model=self.model_name,
                provider="mistral",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
            )
            return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I apologize, but I encountered an error while generating the answer."

    # def summarize_text(self, text: str) -> str:
    #     """Generate a summary of the given text using chat completion."""
    #     prompt = self.summary_template.format(text=text)
    #     try:
    #         resp = completion(
    #             model=self.model_name,
    #             provider="mistral",
    #             messages=[{"role": "user", "content": prompt}],
    #             max_tokens=256,
    #         )
    #         return resp['choices'][0]['message']['content'].strip()
    #     except Exception as e:
    #         logger.error(f"Error generating summary: {e}")
    #         return "I apologize, but I encountered an error while generating the summary."

    def summarize_text(self, text: str) -> str:
        """Generate a summary of the given text using the ChatLiteLLM instance."""
        prompt = self.summary_template.format(text=text)
        try:
            # Prepare the messages for the chat model
            messages = [{"role": "user", "content": prompt}]
            # Use the ChatLiteLLM instance to generate the summary
            response = self.llm.invoke(messages)
            # Extract and return the content from the response
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "I apologize, but I encountered an error while generating the summary."

    def generate_quiz(self, text: str) -> List[Dict[str, str]]:
        """Generate quiz questions and answers from the text using chat completion."""
        prompt = self.quiz_template.format(text=text)
        try:
            resp = completion(
                model=self.model_name,
                provider="mistral",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
            )
            content = resp['choices'][0]['message']['content']
            qa_pairs = []
            current_q, current_a = None, None
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                lower = line.lower()
                if lower.startswith(('q', 'question')):
                    if current_q and current_a:
                        qa_pairs.append({'question': current_q, 'answer': current_a})
                    current_q = line.split(':', 1)[1].strip()
                    current_a = None
                elif lower.startswith(('a', 'answer')):
                    current_a = line.split(':', 1)[1].strip()
            if current_q and current_a:
                qa_pairs.append({'question': current_q, 'answer': current_a})
            return qa_pairs
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return []
