import sys
import os

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from main import main

def run_pipeline():
    try:
        main()
        return {"status": "Pipeline executed successfully"}
    except Exception as e:
        return {"error": str(e)}