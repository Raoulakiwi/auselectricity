#!/usr/bin/env python3
"""
Startup script for the Australian Electricity Market Dashboard backend
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Add the backend directory to Python path
    backend_dir = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_dir))
    
    # Railway environment configuration
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Set environment variables
    os.environ.setdefault("DATABASE_URL", "sqlite:///./electricity_data.db")
    
    # Import and run the FastAPI app
    try:
        from backend.api.main import app
        import uvicorn
        
        print("🚀 Starting Australian Electricity Market Dashboard API...")
        print(f"📊 Server will be available at: http://{host}:{port}")
        print(f"📖 API documentation at: http://{host}:{port}/docs")
        print("🔄 Press Ctrl+C to stop the server")
        
        # Railway-compatible server configuration
        is_production = os.getenv("RAILWAY_ENVIRONMENT_NAME") is not None
        
        uvicorn.run(
            "backend.api.main:app",
            host=host,
            port=port,
            reload=not is_production,  # Disable reload in production
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
