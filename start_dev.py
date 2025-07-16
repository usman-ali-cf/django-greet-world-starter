
#!/usr/bin/env python3
"""
Development startup script for the Electrical Project Manager
Starts both FastAPI backend and React frontend in development mode
"""
import subprocess
import os
import sys
import time
from threading import Thread

def run_fastapi():
    """Run FastAPI backend"""
    print("🚀 Starting FastAPI backend on port 8000...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'], check=True)
    except KeyboardInterrupt:
        print("\n🚀 FastAPI backend stopped.")

def run_react():
    """Run React frontend"""
    print("⚛️  Starting React frontend on port 8080...")
    time.sleep(2)  # Wait a bit for FastAPI to start
    try:
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except KeyboardInterrupt:
        print("\n⚛️  React frontend stopped.")

def main():
    """Main function to start both services"""
    print("🚀 Starting Electrical Project Manager Development Environment")
    print("=" * 60)
    
    # Start FastAPI backend in a separate thread
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Start React frontend in main thread
    try:
        run_react()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down development environment...")
        print("✅ All services stopped.")

if __name__ == '__main__':
    main()
