#!/usr/bin/env python3
"""
MediDrishti AI - Complete Debugging & Testing Script
This script performs comprehensive checks and tests all modules
"""

import os
import sys
from pathlib import Path

print("\n" + "="*70)
print("  MediDrishti AI - Complete Debug & Analysis Report")
print("="*70 + "\n")

# ============================================================================
# SECTION 1: Environment Check
# ============================================================================
print("📋 SECTION 1: Environment Verification")
print("-" * 70)

try:
    python_version = sys.version_info
    print(f"✅ Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ ERROR: Python 3.8+ required!")
        sys.exit(1)
except Exception as e:
    print(f"❌ Python check failed: {e}")
    sys.exit(1)

# Check virtual environment
venv = os.getenv('VIRTUAL_ENV')
if venv:
    print(f"✅ Virtual Environment: {venv}")
else:
    print("⚠️  No virtual environment detected (activate venv first)")

print()

# ============================================================================
# SECTION 2: Project Structure Check
# ============================================================================
print("📁 SECTION 2: Project Structure")
print("-" * 70)

required_dirs = [
    "backend",
    "frontend", 
    "tests",
    "assets",
    "utils"
]

required_files = [
    "app.py",
    "requirements.txt",
    ".env",
    ".env.example"
]

all_dirs_exist = True
for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"✅ {dir_name}/")
    else:
        print(f"❌ {dir_name}/ (MISSING)")
        all_dirs_exist = False

print()

all_files_exist = True
for file_name in required_files:
    file_path = Path(file_name)
    if file_path.exists():
        print(f"✅ {file_name}")
    else:
        print(f"❌ {file_name} (MISSING)")
        all_files_exist = False

print()

# ============================================================================
# SECTION 3: Dependencies Check
# ============================================================================
print("📦 SECTION 3: Dependencies Verification")
print("-" * 70)

required_packages = {
    "streamlit": "Streamlit",
    "langchain": "LangChain",
    "pdfplumber": "PDFPlumber",
    "PyPDF2": "PyPDF2",
    "PIL": "Pillow",
    "dotenv": "python-dotenv",
    "pytest": "pytest",
}

optional_packages = {
    "langchain_openai": "langchain-openai",
    "easyocr": "EasyOCR",
}

all_deps_ok = True
print("REQUIRED PACKAGES:")
for import_name, display_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"  ✅ {display_name}")
    except ImportError:
        print(f"  ❌ {display_name} (NOT INSTALLED)")
        all_deps_ok = False

print("\nOPTIONAL PACKAGES:")
for import_name, display_name in optional_packages.items():
    try:
        __import__(import_name)
        print(f"  ✅ {display_name}")
    except ImportError:
        print(f"  ⚠️  {display_name} (optional, not installed)")

print()

# ============================================================================
# SECTION 4: Configuration Check
# ============================================================================
print("⚙️  SECTION 4: Configuration")
print("-" * 70)

# Check .env file
env_file = Path(".env")
if env_file.exists():
    print("✅ .env file exists")
    with open(env_file, 'r') as f:
        content = f.read()
        if "OPENAI_API_KEY" in content:
            if "sk-" in content or "your-" not in content:
                print("✅ OPENAI_API_KEY is configured")
            else:
                print("⚠️  OPENAI_API_KEY not set (shows placeholder)")
        else:
            print("❌ OPENAI_API_KEY not found in .env")
else:
    print("❌ .env file not found")

print()

# ============================================================================
# SECTION 5: Backend Module Tests
# ============================================================================
print("🔧 SECTION 5: Backend Modules Import Test")
print("-" * 70)

backend_modules = [
    ("backend.analyzer", "Analyzer Module"),
    ("backend.report_parser", "Report Parser"),
    ("backend.health_score", "Health Score"),
    ("backend.diet_engine", "Diet Engine"),
    ("backend.precaution_engine", "Precaution Engine"),
    ("backend.prompts", "Prompts"),
    ("backend.chatbot", "Chatbot"),
]

all_modules_ok = True
for module_name, display_name in backend_modules:
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
    except Exception as e:
        print(f"❌ {display_name}")
        print(f"   Error: {str(e)[:60]}...")
        all_modules_ok = False

print()

# ============================================================================
# SECTION 6: Frontend Import Test
# ============================================================================
print("🎨 SECTION 6: Frontend Modules Import Test")
print("-" * 70)

frontend_modules = [
    ("frontend.ui", "UI Components"),
]

for module_name, display_name in frontend_modules:
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
    except Exception as e:
        print(f"❌ {display_name}")
        print(f"   Error: {str(e)[:60]}...")

print()

# ============================================================================
# SECTION 7: Functional Tests
# ============================================================================
print("🧪 SECTION 7: Functional Tests")
print("-" * 70)

# Test 1: Report Parser
try:
    from backend.report_parser import validate_report_file, parse_medical_parameters
    
    # Test file validation
    assert validate_report_file("report.pdf") == True, "PDF validation failed"
    assert validate_report_file("report.txt") == False, "TXT validation should fail"
    
    # Test parameter parsing
    text = "Hemoglobin: 14.5 g/dL"
    result = parse_medical_parameters(text)
    
    print("✅ Report Parser - All tests passed")
except Exception as e:
    print(f"❌ Report Parser - {str(e)}")

# Test 2: Analyzer
try:
    from backend.analyzer import analyze_parameters, generate_health_summary
    
    parsed = {"hemoglobin": "14.5"}
    results = analyze_parameters(parsed)
    
    assert len(results) > 0, "No analysis results"
    assert "status" in results[0], "Missing status field"
    
    summary = generate_health_summary(results)
    assert "health_score" in summary, "Missing health_score"
    
    print("✅ Analyzer - All tests passed")
except Exception as e:
    print(f"❌ Analyzer - {str(e)}")

# Test 3: Health Score
try:
    from backend.health_score import calculate_health_score, risk_level
    
    parameters = [{"parameter": "Test", "status": "Normal"}]
    score = calculate_health_score(parameters)
    
    assert 0 <= score <= 100, "Invalid health score"
    
    level = risk_level(score)
    assert level in ["Low", "Moderate", "High"], "Invalid risk level"
    
    print("✅ Health Score - All tests passed")
except Exception as e:
    print(f"❌ Health Score - {str(e)}")

# Test 4: Diet Engine
try:
    from backend.diet_engine import generate_diet_recommendations
    
    parameters = [{"parameter": "Hemoglobin", "status": "Low"}]
    diet = generate_diet_recommendations(parameters)
    
    assert "include" in diet, "Missing include"
    assert "limit" in diet, "Missing limit"
    
    print("✅ Diet Engine - All tests passed")
except Exception as e:
    print(f"❌ Diet Engine - {str(e)}")

# Test 5: Precaution Engine
try:
    from backend.precaution_engine import generate_precaution_plan
    
    parameters = [{"parameter": "Cholesterol", "status": "High"}]
    plan = generate_precaution_plan(parameters)
    
    assert "daily_precautions" in plan, "Missing precautions"
    
    print("✅ Precaution Engine - All tests passed")
except Exception as e:
    print(f"❌ Precaution Engine - {str(e)}")

# Test 6: Chatbot (without API call)
try:
    from backend.chatbot import OpenAIClient
    
    client = OpenAIClient(api_key="test-key")
    assert client.api_key == "test-key", "API key not set"
    assert client.model_name == "gpt-4-turbo", "Wrong model"
    
    print("✅ Chatbot Client - All tests passed")
except Exception as e:
    print(f"❌ Chatbot Client - {str(e)}")

print()

# ============================================================================
# SECTION 8: Summary & Recommendations
# ============================================================================
print("📊 SECTION 8: Summary & Recommendations")
print("-" * 70)

if all_deps_ok and all_modules_ok and all_dirs_exist and all_files_exist:
    print("\n🎉 ALL CHECKS PASSED! Ready to run.\n")
    print("✅ Environment setup correctly")
    print("✅ All dependencies installed")
    print("✅ All modules import successfully")
    print("✅ Project structure complete")
    print("\n🚀 NEXT STEP: Run the application with:")
    print("   streamlit run app.py")
    print()
else:
    print("\n⚠️  ISSUES FOUND - Follow recommendations below:\n")
    
    if not all_deps_ok:
        print("1️⃣  INSTALL MISSING DEPENDENCIES:")
        print("   pip install -r requirements.txt\n")
    
    if not all_modules_ok:
        print("2️⃣  FIX MODULE IMPORT ERRORS:")
        print("   - Check Python imports in backend modules")
        print("   - Ensure all files have proper __init__.py\n")
    
    if not all_files_exist:
        print("3️⃣  CREATE MISSING FILES:")
        print("   - Run: python setup_dirs.py\n")

print("="*70)
print("Debug report completed!")
print("="*70 + "\n")
