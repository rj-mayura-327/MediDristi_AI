# MediDrishti AI - Quick Start Guide

Get MediDrishti AI running in 5 minutes!

## 🚀 TL;DR (Quick Setup)

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run application
streamlit run app.py

# 5. Open browser
# → http://localhost:8501
```

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key (free at https://aistudio.google.com/app/apikey)
- ~500MB disk space
- Modern web browser

## 🔑 Getting Your API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the key

## ✅ Installation Steps

### Step 1: Verify Python

```bash
python --version
# Should show Python 3.8+
```

If not installed, download from https://www.python.org/

### Step 2: Navigate to Project

```bash
cd MediDrishtiAI
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` in your terminal prompt when activated.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. Watch for the ✓ checkmarks.

### Step 5: Configure API Key

**Windows (PowerShell/CMD):**
```bash
cp .env.example .env
# Edit .env with your favorite editor and add API key
# Or use:
echo GOOGLE_API_KEY=your_key_here > .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env  # Edit with your API key
# Then press Ctrl+O, Enter, Ctrl+X to save
```

The `.env` file should look like:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 6: Verify Installation

```bash
python verify_setup.py
```

You should see all green checkmarks ✅

### Step 7: Run Application

```bash
streamlit run app.py
```

You'll see output like:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.xxx:8501
```

### Step 8: Open in Browser

Automatically opens, or manually go to: http://localhost:8501

## 🎯 Using the Application

### 1. Upload Your Medical Report
- Click "Upload Report" in the sidebar
- Select a PDF or image file
- Wait for analysis (usually 5-30 seconds)

### 2. View Results
- **Analysis Dashboard**: See health score and findings
- **Diet Recommendations**: Get personalized food guidance
- **Precautions**: Learn daily health tips
- **Chat**: Ask questions about your report
- **Download**: Save summary as text file

## 🆘 Troubleshooting

### "Module not found" Error
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### "GOOGLE_API_KEY not set"
```bash
# Check if .env file exists
ls .env  # macOS/Linux
dir .env  # Windows

# Make sure it has your key:
GOOGLE_API_KEY=your_actual_key_not_text
```

### Port 8501 Already in Use
```bash
streamlit run app.py --server.port 8502
# Then open: http://localhost:8502
```

### Application Crashes After Upload
- Try a smaller PDF
- Check available system memory
- Check that PDFPlumber is installed: `pip install pdfplumber`

### Can't Install EasyOCR
```bash
# It's optional - PDFPlumber will still work
# For image reports, you may need to install manually:
pip install easyocr opencv-python-headless
```

## 📁 File Structure

```
MediDrishtiAI/
├── app.py                 ← Main application (run this)
├── requirements.txt       ← Dependencies
├── .env                   ← Your API key (DO NOT COMMIT)
├── .env.example          ← Template
├── backend/
│   ├── analyzer.py       ← Medical analysis
│   ├── chatbot.py        ← Chat assistant
│   ├── diet_engine.py    ← Diet recommendations
│   └── ...
├── frontend/
│   └── ui.py             ← UI components
└── assets/
    └── style.css         ← Styling
```

## 🔒 Security Notes

✅ **Safe to Use**:
- API key stored locally in `.env`
- No data sent to external databases
- Reports only processed in your session
- No permanent file storage

⚠️ **Keep Safe**:
- Never share your `.env` file
- Never push `.env` to GitHub
- Keep your API key secret
- Add `.env` to `.gitignore` (already done)

## 📞 Need Help?

1. **Check the README.md** for detailed documentation
2. **Run verify_setup.py** to diagnose issues
3. **Check logs**: Streamlit shows detailed error messages
4. **Review DEPLOYMENT.md** for advanced setup

## 🚀 Next Steps

After getting running:

1. **Try sample reports**: Create test medical reports
2. **Explore all pages**: Go through each feature
3. **Test the chat**: Ask it questions about your report
4. **Download summary**: Try exporting results

## 🌐 Deploy to Cloud (Optional)

Want to share with others? See **DEPLOYMENT.md** for:
- Streamlit Cloud (free, easiest)
- Docker (any server)
- AWS, GCP, Azure
- Your own server

## 💡 Tips

- Streamlit automatically reloads on code changes
- Use clear, simple medical reports for best results
- Larger PDFs take longer to process
- Chat assistant works best with specific questions
- Results are estimates - consult doctors for medical decisions

## 📚 Resources

- **LangChain Docs**: https://docs.langchain.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Google Gemini API**: https://ai.google.dev/
- **Python Help**: https://www.python.org/

## ⚕️ Medical Disclaimer

**MediDrishti AI is NOT a doctor.**

- For emergency symptoms, call 911
- Always consult qualified healthcare providers
- Use results for understanding only
- Don't make medical decisions based solely on this app

---

**Happy analyzing! 🩺**

Still stuck? Run: `python verify_setup.py` for diagnostics.
