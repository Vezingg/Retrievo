import streamlit as st
import requests
import json
import os
from typing import List, Dict, Union

# API endpoint
API_URL = "http://localhost:8000"

def main():
    st.title("RAG Pipeline - Q&A, Summarization & Quizzes")
    
    # Sidebar for document upload
    st.sidebar.header("Document Upload")
    
    # PDF upload
    pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file:
        if st.sidebar.button("Process PDF"):
            files = {"file": (pdf_file.name, pdf_file.getvalue())}
            response = requests.post(f"{API_URL}/upload/pdf", files=files)
            if response.status_code == 200:
                st.sidebar.success("PDF processed successfully!")
            else:
                st.sidebar.error("Error processing PDF")
    
    # URL input
    url = st.sidebar.text_input("Enter webpage URL")
    if url and st.sidebar.button("Process URL"):
        response = requests.post(f"{API_URL}/process/url", json={"url": url})
        if response.status_code == 200:
            st.sidebar.success("URL processed successfully!")
        else:
            st.sidebar.error("Error processing URL")
    
    # Main content area
    st.header("Ask Questions")
    
    # Query input
    query = st.text_input("Enter your question or request (e.g., 'Summarize the document' or 'Generate a quiz')")
    
    if query:
        if st.button("Submit"):
            # Process query
            response = requests.post(f"{API_URL}/query", json={"query": query})
            
            if response.status_code == 200:
                result = response.json()
                
                if result["type"] == "quiz":
                    st.header("Quiz Questions")
                    for i, qa in enumerate(result["questions"], 1):
                        st.subheader(f"Question {i}")
                        st.write(qa["question"])
                        
                        # Answer input
                        user_answer = st.text_input(f"Your answer for Question {i}", key=f"answer_{i}")
                        
                        if user_answer:
                            if st.button(f"Check Answer {i}", key=f"check_{i}"):
                                feedback = requests.post(
                                    f"{API_URL}/quiz/check",
                                    json={
                                        "question": qa["question"],
                                        "user_answer": user_answer,
                                        "correct_answer": qa["answer"]
                                    }
                                ).json()
                                
                                if feedback["is_correct"]:
                                    st.success("Correct!")
                                else:
                                    st.error("Incorrect")
                                st.write(feedback["feedback"])
                
                elif result["type"] == "summary":
                    st.header("Summary")
                    st.write(result["content"])
                
                else:  # answer
                    st.header("Answer")
                    st.write(result["content"])
            
            else:
                st.error("Error processing query")

if __name__ == "__main__":
    main() 