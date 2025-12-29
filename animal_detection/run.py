import uvicorn
import os
import sys

# Add the current directory to sys.path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Animal Detection API...")
    # Using "src.main:app" string allows reloading to work
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
