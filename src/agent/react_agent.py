from typing import List, Dict, Union, Tuple
import logging
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from .tools import DocumentSearchTool, SummarizationTool, QuizGenerationTool
from ..generation.llm import LLMGenerator
from ..retrieval.vector_store import VectorStore
from ..ingestion.embedding_generator import EmbeddingGenerator
from langchain.tools import Tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReActAgent:
    """ReAct agent for handling complex queries using tools."""
    
    def __init__(self, vector_store: VectorStore, embedder: EmbeddingGenerator, llm_generator: LLMGenerator):
        """
        Initialize the ReAct agent.
        
        Args:
            vector_store: Vector store instance
            embedder: Embedding generator instance
            llm_generator: LLM generator instance
        """
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm_generator = llm_generator
        
        # Initialize tools
        self.search_tool = DocumentSearchTool(vector_store, embedder)
        self.summarize_tool = SummarizationTool(llm_generator)
        self.quiz_tool = QuizGenerationTool(llm_generator)
        
        # Initialize LangChain agent
        # wrap each tool in langchain.tools.Tool so it has .is_single_input, etc.
        tools = [
            Tool(
                name="search_documents",
                func=self.search_tool.search,
                description="Search for relevant documents in the knowledge base"
            ),
            Tool(
                name="summarize",
                func=self.summarize_tool.summarize,
                description="Summarize a given text"
            ),
            Tool(
                name="generate_quiz",
                func=self.quiz_tool.generate_quiz,
                description="Generate quiz questions from text"
            ),
        ]
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm_generator.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    def process_query(self, query: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Process a user query using the ReAct agent.
        
        Args:
            query: User query
            
        Returns:
            Dictionary containing the response and any additional data
        """
        try:
            # Run the agent
            response = self.agent.run(query)
            
            # Parse the response based on the type of query
            if "quiz" in query.lower():
                # Extract quiz questions from the response
                quiz_questions = self.quiz_tool.generate_quiz(response)
                return {
                    "type": "quiz",
                    "questions": quiz_questions
                }
            elif "summarize" in query.lower():
                return {
                    "type": "summary",
                    "content": response
                }
            else:
                return {
                    "type": "answer",
                    "content": response
                }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "type": "error",
                "content": "I apologize, but I encountered an error while processing your query."
            }
    
    def check_answer(self, question: str, user_answer: str, correct_answer: str) -> Dict[str, str]:
        """
        Check a user's answer to a quiz question.
        
        Args:
            question: The quiz question
            user_answer: User's answer
            correct_answer: Correct answer
            
        Returns:
            Dictionary containing feedback and explanation
        """
        try:
            # Generate feedback using the LLM
            prompt = f"""Question: {question}
User's Answer: {user_answer}
Correct Answer: {correct_answer}

Provide feedback on the user's answer. If it's incorrect, explain why and provide the correct answer. Be encouraging and helpful."""

            feedback = self.llm_generator.llm(prompt)
            
            return {
                "feedback": feedback.strip(),
                "is_correct": user_answer.lower().strip() == correct_answer.lower().strip()
            }
        except Exception as e:
            logger.error(f"Error checking answer: {str(e)}")
            return {
                "feedback": "I apologize, but I encountered an error while checking your answer.",
                "is_correct": False
            } 