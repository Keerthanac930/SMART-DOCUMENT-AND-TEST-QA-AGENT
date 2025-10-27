#!/usr/bin/env python3
"""
Frontend runner for Smart Document QA Agent
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit frontend application"""
    # Set environment variables
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.headless', 'true'
    ])

if __name__ == "__main__":
    main()
