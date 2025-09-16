from fastapi import APIRouter, BackgroundTasks, HTTPException
from datetime import datetime
import asyncio
import subprocess
import sys
import os

router = APIRouter()

# Global variable to track scraper status
scraper_status = {
    "is_running": False,
    "last_run": None,
    "last_error": None,
    "progress": "Ready to collect data"
}

def run_data_collection():
    """Run the data collection script in the background"""
    global scraper_status
    
    try:
        scraper_status["is_running"] = True
        scraper_status["progress"] = "Starting data collection..."
        scraper_status["last_error"] = None
        
        # Change to the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        # Run the real-only data collection script
        result = subprocess.run(
            [sys.executable, "collect_real_only_data.py"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            scraper_status["progress"] = "Data collection completed successfully!"
            scraper_status["last_run"] = datetime.now().isoformat()
        else:
            scraper_status["progress"] = f"Data collection failed: {result.stderr}"
            scraper_status["last_error"] = result.stderr
            
    except subprocess.TimeoutExpired:
        scraper_status["progress"] = "Data collection timed out after 5 minutes"
        scraper_status["last_error"] = "Timeout"
    except Exception as e:
        scraper_status["progress"] = f"Data collection error: {str(e)}"
        scraper_status["last_error"] = str(e)
    finally:
        scraper_status["is_running"] = False

@router.post("/start")
async def start_data_collection(background_tasks: BackgroundTasks):
    """Start the data collection process"""
    global scraper_status
    
    if scraper_status["is_running"]:
        raise HTTPException(
            status_code=400, 
            detail="Data collection is already running. Please wait for it to complete."
        )
    
    # Start the data collection in the background
    background_tasks.add_task(run_data_collection)
    
    return {
        "message": "Data collection started",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/status")
async def get_scraper_status():
    """Get the current status of the data collection process"""
    return {
        "is_running": scraper_status["is_running"],
        "last_run": scraper_status["last_run"],
        "last_error": scraper_status["last_error"],
        "progress": scraper_status["progress"],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
