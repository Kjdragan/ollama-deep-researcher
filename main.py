import subprocess
import sys
from pathlib import Path

def main():
    # Ensure we're in a virtual environment
    if not sys.prefix != sys.base_prefix:
        print("Please run this script in your virtual environment.")
        sys.exit(1)
    
    # Ensure we're in the project root directory
    project_root = Path(__file__).parent
    if not (project_root / "pyproject.toml").exists():
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    try:
        print("Starting LangGraph server...")
        subprocess.check_call([
            "uvx",
            "--refresh",
            "--from", "langgraph-cli[inmem]",
            "--with-editable", ".",
            "--python", "3.11",
            "langgraph", "dev"
        ])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
