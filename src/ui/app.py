import streamlit as st
import requests
import json
import os
from typing import List, Dict, Union

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.set_page_config(
    page_title="Retrievo - Smart Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .result-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .success-message {
        color: #4CAF50;
        font-weight: bold;
    }
    .error-message {
        color: #f44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://img.icons8.com/color/96/000000/book.png", width=80)
    with col2:
        st.title("Retrievo - Smart Document Assistant")
        st.markdown("Your intelligent document analysis and Q&A companion")

    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Upload")
        
        # PDF upload section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📑 Upload PDF")
        pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if pdf_file:
            if st.button("Process PDF", key="process_pdf"):
                with st.spinner("Processing PDF..."):
                    files = {"file": (pdf_file.name, pdf_file.getvalue())}
                    response = requests.post(f"{API_URL}/upload/pdf", files=files)
                    if response.status_code == 200:
                        st.success("✅ PDF processed successfully!")
                    else:
                        st.error("❌ Error processing PDF")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # URL input section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("🌐 Process Webpage")
        url = st.text_input("Enter webpage URL")
        if url and st.button("Process URL", key="process_url"):
            with st.spinner("Processing webpage..."):
                response = requests.post(f"{API_URL}/process/url", json={"url": url})
                if response.status_code == 200:
                    st.success("✅ URL processed successfully!")
                else:
                    st.error("❌ Error processing URL")
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content area
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.header("💭 Ask Questions")
    
    # Query input with better styling
    query = st.text_input(
        "Enter your question or request",
        placeholder="e.g., 'Summarize the document' or 'Generate a quiz'",
        help="You can ask questions, request summaries, or generate quizzes"
    )
    
    if query:
        if st.button("Submit Query", key="submit_query"):
            with st.spinner("Processing your request..."):
                # Process query
                response = requests.post(f"{API_URL}/query", json={"query": query})
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["type"] == "quiz":
                        st.header("📝 Quiz Questions")
                        for i, qa in enumerate(result["questions"], 1):
                            st.markdown(f"### Question {i}")
                            st.markdown(f"**{qa['question']}**")
                            
                            # Answer input with better styling
                            user_answer = st.text_input(
                                f"Your answer for Question {i}",
                                key=f"answer_{i}",
                                placeholder="Type your answer here..."
                            )
                            
                            if user_answer:
                                if st.button(f"Check Answer {i}", key=f"check_{i}"):
                                    with st.spinner("Checking answer..."):
                                        feedback = requests.post(
                                            f"{API_URL}/quiz/check",
                                            json={
                                                "question": qa["question"],
                                                "user_answer": user_answer,
                                                "correct_answer": qa["answer"]
                                            }
                                        ).json()
                                        
                                        if feedback["is_correct"]:
                                            st.success("✅ Correct!")
                                        else:
                                            st.error("❌ Incorrect")
                                        st.markdown(f"**Feedback:** {feedback['feedback']}")
                    
                    elif result["type"] == "summary":
                        st.header("📋 Summary")
                        st.markdown(result["content"])
                    
                    else:  # answer
                        st.header("💡 Answer")
                        st.markdown(result["content"])
                
                else:
                    st.error("❌ Error processing query")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 