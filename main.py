import subprocess
import sys
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if MISTRAL_API_KEY is set
    if not os.getenv("MISTRAL_API_KEY"):
        print("Error: MISTRAL_API_KEY environment variable not set")
        print("Please create a .env file with your Mistral API key")
        sys.exit(1)
    
    try:
        # Start FastAPI backend
        api_process = subprocess.Popen(
            ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Started FastAPI backend on http://localhost:8000")
        
        # Start Streamlit frontend
        ui_process = subprocess.Popen(
            ["streamlit", "run", "src/ui/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Started Streamlit frontend")
        
        # Wait for processes
        api_process.wait()
        ui_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        api_process.terminate()
        ui_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 

#  streamlit run src/ui/app.py