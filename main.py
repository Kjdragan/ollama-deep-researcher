"""Entry point for the Ollama Deep Researcher application.

This module provides the main entry point for running the LangGraph-based research assistant.
It handles environment setup and server initialization."""

from pathlib import Path
import subprocess
import sys

def main() -> None:
    """Run the LangGraph development server with proper environment setup.
    
    Ensures the application is running in a virtual environment and from the correct
    directory before starting the LangGraph server.
    
    Returns:
        None
    
    Raises:
        SystemExit: If environment checks fail or if server fails to start.
    """
    # Ensure we're in a virtual environment
    if not sys.prefix != sys.base_prefix:
        sys.exit("Please run this script in your virtual environment.")
    
    # Ensure we're in the project root directory
    project_root = Path(__file__).parent
    if not (project_root / "pyproject.toml").exists():
        sys.exit("Please run this script from the project root directory.")
    
    try:
        sys.stdout.write("Starting LangGraph server...\n")
        subprocess.check_call([
            "uvx",
            "--refresh",
            "--from", "langgraph-cli[inmem]",
            "--with-editable", ".",
            "--python", "3.11",
            "langgraph", "dev"
        ])
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
