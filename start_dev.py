
#!/usr/bin/env python3
"""
Development startup script for the Electrical Project Manager
Starts both Flask backend and React frontend in development mode
"""
import subprocess
import os
import sys
import time
from threading import Thread

def run_flask():
    """Run Flask backend"""
    print("🔧 Starting Flask backend on port 5000...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'flask_api_adapter.py'], check=True)
    except KeyboardInterrupt:
        print("\n🔧 Flask backend stopped.")

def run_react():
    """Run React frontend"""
    print("⚛️  Starting React frontend on port 5173...")
    time.sleep(2)  # Wait a bit for Flask to start
    try:
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except KeyboardInterrupt:
        print("\n⚛️  React frontend stopped.")

def main():
    """Main function to start both services"""
    print("🚀 Starting Electrical Project Manager Development Environment")
    print("=" * 60)
    
    # Start Flask backend in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start React frontend in main thread
    try:
        run_react()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down development environment...")
        print("✅ All services stopped.")

if __name__ == '__main__':
    main()
