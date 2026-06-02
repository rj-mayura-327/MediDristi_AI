# MediDrishti AI - Command Reference

Quick reference for common commands and operations.

## 🚀 Quick Start Commands

### One-Time Setup
```bash
# Clone/navigate to project
cd MediDrishtiAI

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate                    # Windows
source venv/bin/activate                 # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add GOOGLE_API_KEY

# Verify installation
python verify_setup.py
```

### Run Application
```bash
# Make sure virtual environment is activated first
streamlit run app.py
```

### Access Application
- **Default URL**: http://localhost:8501
- **Custom Port**: `streamlit run app.py --server.port 8502`

---

## 🧪 Testing Commands

### Run All Tests
```bash
pytest tests/
```

### Run Tests with Coverage
```bash
pytest --cov=backend tests/
```

### Run Specific Test
```bash
pytest tests/test_backend.py::TestAnalyzer::test_analyze_parameters_normal
```

### Run Tests in Verbose Mode
```bash
pytest -v tests/
```

### Generate Coverage HTML Report
```bash
pytest --cov=backend --cov-report=html tests/
# Open htmlcov/index.html in browser
```

---

## 🔧 Development Commands

### Code Formatting
```bash
# Format all code
black .

# Format specific file
black app.py
```

### Linting Checks
```bash
# Check all code
flake8 .

# Check specific directory
flake8 backend/
```

### Type Checking
```bash
# Check all code
mypy .

# Check specific file
mypy app.py
```

### Pre-commit Check (All At Once)
```bash
black . && flake8 . && mypy . && pytest tests/
```

---

## 📦 Dependency Management

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install With Dev Tools
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### List Installed Packages
```bash
pip list
```

### Freeze Dependencies
```bash
pip freeze > requirements.txt
```

---

## 🌐 Deployment Commands

### Local Deployment
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment
```bash
# Push to GitHub first
git push origin main

# Then deploy via web UI at https://streamlit.io/cloud
```

### Docker Deployment
```bash
# Build Docker image
docker build -t medidristi-ai .

# Run Docker container
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key medidristi-ai

# Push to Docker Hub
docker tag medidristi-ai:latest YOUR_USERNAME/medidristi-ai:latest
docker push YOUR_USERNAME/medidristi-ai:latest
```

---

## 📁 File & Directory Operations

### Create Directories
```bash
python setup_dirs.py
```

### View Directory Structure
```bash
# Windows
tree /F

# macOS/Linux
tree -L 2
```

### List Project Files
```bash
# Windows
dir /s

# macOS/Linux
ls -la
```

---

## 📝 Git Operations

### Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: MediDrishti AI"
```

### Create New Branch
```bash
git checkout -b feature/your-feature-name
```

### Push Changes
```bash
git push origin main
```

### View Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

---

## 🔐 Environment & Configuration

### View Environment Variables
```bash
# Windows PowerShell
Get-ChildItem Env:GOOGLE_API_KEY

# Windows CMD
echo %GOOGLE_API_KEY%

# macOS/Linux
echo $GOOGLE_API_KEY
```

### Set Environment Variable (Temporary)
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY = "your_key"

# macOS/Linux
export GOOGLE_API_KEY=your_key
```

### Edit Configuration Files
```bash
# Edit .env file
nano .env                              # macOS/Linux
notepad .env                           # Windows
code .env                              # VS Code

# Edit Streamlit config
nano ~/.streamlit/config.toml          # macOS/Linux
```

---

## 🐛 Debugging & Troubleshooting

### Verify Setup
```bash
python verify_setup.py
```

### Check Python Version
```bash
python --version
python -c "import sys; print(sys.executable)"
```

### Check Module Installation
```bash
python -c "import streamlit; print(streamlit.__version__)"
python -c "import langchain; print(langchain.__version__)"
```

### Clear Streamlit Cache
```bash
streamlit cache clear
```

### Run with Debug Logging
```bash
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py
```

### Check Port in Use (macOS/Linux)
```bash
lsof -i :8501
```

### Kill Process on Port (macOS/Linux)
```bash
kill -9 $(lsof -t -i :8501)
```

---

## 📊 Monitoring & Performance

### Check Memory Usage
```bash
# macOS/Linux
top -p $(pgrep streamlit)

# Windows
tasklist | findstr streamlit
```

### Profiling Python Code
```bash
python -m cProfile -s cumtime app.py
```

### View Logs
```bash
cat app.log                            # macOS/Linux
type app.log                           # Windows
tail -f app.log                        # Watch live (macOS/Linux)
```

---

## 🚀 Advanced Commands

### Run Streamlit With Custom Settings
```bash
streamlit run app.py \
  --server.port 8501 \
  --server.address localhost \
  --logger.level=debug \
  --client.showErrorDetails=false
```

### Update All Packages Safely
```bash
pip list --outdated
pip install --upgrade package_name
```

### Generate Requirements From Installed Packages
```bash
pip freeze | grep -E "streamlit|langchain|pdfplumber" > requirements.txt
```

### Run Python Script
```bash
python script.py
python -m pytest tests/
```

### Interactive Python Shell
```bash
python
>>> from backend.analyzer import analyze_parameters
>>> analyze_parameters({"hemoglobin": "12.5"})
```

---

## 📖 Help & Documentation

### View Help
```bash
# Streamlit help
streamlit --help
streamlit run --help

# pytest help
pytest --help

# Python help
python -h
```

### Open Documentation
```bash
# Open README
cat README.md

# Open QUICKSTART
cat QUICKSTART.md

# Open ARCHITECTURE
cat ARCHITECTURE.md
```

---

## 🔄 Common Workflows

### Daily Development Workflow
```bash
# 1. Activate environment
source venv/bin/activate            # or venv\Scripts\activate

# 2. Make changes
# ... edit files ...

# 3. Run tests
pytest tests/

# 4. Format code
black .

# 5. Check style
flake8 .

# 6. Run app to test
streamlit run app.py

# 7. Commit changes
git add .
git commit -m "Meaningful message"
git push
```

### Pre-Deployment Checklist
```bash
# 1. Verify setup
python verify_setup.py

# 2. Run all tests
pytest tests/

# 3. Code quality checks
black . && flake8 . && mypy .

# 4. Update dependencies
pip freeze > requirements.txt

# 5. Build/test Docker
docker build -t medidristi-ai .
docker run -p 8501:8501 -e GOOGLE_API_KEY=test medidristi-ai

# 6. Push to GitHub
git push origin main

# 7. Deploy to platform
# ... follow deployment docs ...
```

### Troubleshooting Workflow
```bash
# 1. Run verification
python verify_setup.py

# 2. Check Python environment
python --version
which python                          # macOS/Linux

# 3. Check dependencies
pip list | grep -E "streamlit|langchain"

# 4. Check .env configuration
cat .env

# 5. Check logs/errors
# Look at terminal output carefully

# 6. Test individual modules
python -c "from backend.analyzer import analyze_parameters; print('OK')"

# 7. Run with debug
streamlit run app.py --logger.level=debug
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Setup Environment | `python -m venv venv` |
| Activate Environment | `venv\Scripts\activate` |
| Install Dependencies | `pip install -r requirements.txt` |
| Start App | `streamlit run app.py` |
| Run Tests | `pytest tests/` |
| Format Code | `black .` |
| Lint Code | `flake8 .` |
| Check Types | `mypy .` |
| Verify Setup | `python verify_setup.py` |
| Clear Cache | `streamlit cache clear` |
| View Logs | `tail -f app.log` |

---

## 💡 Pro Tips

1. **Use virtual environment always** - Prevents package conflicts
2. **Commit frequently** - Small, focused commits are easier to review
3. **Run tests before pushing** - Catch issues early
4. **Update requirements.txt** - Keep dependencies synchronized
5. **Use meaningful commit messages** - Future you will thank you
6. **Check .env is in .gitignore** - Never commit API keys
7. **Test locally first** - Before deploying to production
8. **Monitor resource usage** - Keep an eye on memory/CPU
9. **Keep logs enabled** - Helps with debugging
10. **Document changes** - Update README when adding features

---

## 🆘 Emergency Commands

### Reset Everything
```bash
# Remove and recreate environment
rm -rf venv                           # macOS/Linux
rmdir /s venv                         # Windows

# Recreate and reinstall
python -m venv venv
venv\Scripts\activate                 # Windows
source venv/bin/activate              # macOS/Linux
pip install -r requirements.txt
```

### Force Kill Streamlit
```bash
# Windows
taskkill /F /IM python.exe

# macOS/Linux
pkill -f streamlit
```

### Clear All Cache
```bash
# Streamlit cache
streamlit cache clear

# Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

---

## 📚 Related Documentation

- **Setup**: See QUICKSTART.md
- **Deployment**: See DEPLOYMENT.md
- **Architecture**: See ARCHITECTURE.md
- **Configuration**: See CONFIGURATION.md
- **Contributing**: See CONTRIBUTING.md
- **Troubleshooting**: See README.md

---

**Last Updated**: June 2026

**Version**: 1.0.0
