#!/usr/bin/env python3
"""
MediDrishti AI - System Setup & Verification Script

This script helps with initial setup and verification of the MediDrishti AI system.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required.")
        return False
    print("✅ Python version OK")
    return True


def check_directories():
    """Check if required directories exist."""
    print_header("Checking Directory Structure")
    
    required_dirs = [
        "backend",
        "frontend",
        "utils",
        "assets",
        "tests"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (missing)")
            all_exist = False
    
    return all_exist


def check_files():
    """Check if required files exist."""
    print_header("Checking Required Files")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "backend/analyzer.py",
        "backend/chatbot.py",
        "backend/diet_engine.py",
        "backend/health_score.py",
        "backend/precaution_engine.py",
        "backend/prompts.py",
        "backend/report_parser.py",
        "frontend/ui.py",
        "assets/style.css",
    ]
    
    all_exist = True
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            all_exist = False
    
    return all_exist


def check_env_file():
    """Check if .env file exists."""
    print_header("Checking Environment Configuration")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "GOOGLE_API_KEY" in content:
                if content.strip().endswith("="):
                    print("⚠️  GOOGLE_API_KEY is not set (empty)")
                    return False
                else:
                    print("✅ GOOGLE_API_KEY appears to be configured")
                    return True
            else:
                print("❌ GOOGLE_API_KEY not found in .env")
                return False
    else:
        print("❌ .env file not found")
        print("   Create it with: cp .env.example .env")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    print_header("Checking Python Dependencies")
    
    required_packages = [
        ("streamlit", "Streamlit"),
        ("langchain", "LangChain"),
        ("pdfplumber", "PDFPlumber"),
        ("PyPDF2", "PyPDF2"),
        ("PIL", "Pillow"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_installed = True
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} (not installed)")
            all_installed = False
    
    return all_installed


def recommend_actions(checks):
    """Provide recommendations based on failed checks."""
    print_header("Setup Recommendations")
    
    if not checks['python']:
        print("1. Upgrade Python to 3.8 or higher")
    
    if not checks['directories']:
        print("1. Run: python setup_dirs.py")
    
    if not checks['files']:
        print("2. Ensure all required files are present")
        print("   Check the README.md for the correct file structure")
    
    if not checks['env']:
        print(f"3. Set up environment variables:")
        print(f"   - Copy .env.example to .env")
        print(f"   - Add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey")
    
    if not checks['dependencies']:
        print("4. Install dependencies: pip install -r requirements.txt")


def main():
    """Run all checks."""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        MediDrishti AI - System Setup Verification      ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    checks = {
        'python': check_python_version(),
        'directories': check_directories(),
        'files': check_files(),
        'env': check_env_file(),
        'dependencies': check_dependencies(),
    }
    
    recommend_actions(checks)
    
    print_header("Summary")
    
    if all(checks.values()):
        print("\n✅ All checks passed! Ready to run MediDrishti AI")
        print("\nStart the application with:")
        print("   streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick Setup Steps:")
        print("1. Create virtual environment: python -m venv venv")
        print("2. Activate it: venv\\Scripts\\activate  (Windows)")
        print("               source venv/bin/activate  (Mac/Linux)")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Set up .env: cp .env.example .env")
        print("5. Add your API key to .env")
        print("6. Run: streamlit run app.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
