# MediDrishti AI

**Intelligent AI-powered medical report analysis assistant for better health decisions**

MediDrishti AI is a production-ready healthcare web application that helps users understand their medical reports through intelligent AI analysis, simplified explanations, personalized diet recommendations, and health precautions.

## 🎯 Features

### Core Functionalities

- **📄 Medical Report Upload**
  - Support for PDF, PNG, JPG, JPEG formats
  - Automatic text extraction from reports
  - Image-based report parsing with OCR
  - Robust error handling

- **🔬 AI-Powered Medical Analysis**
  - Extracts key parameters: Hemoglobin, RBC, WBC, Platelets, Blood Sugar, Cholesterol, Vitamin D, Creatinine, Liver & Kidney Parameters
  - Provides medical and simplified explanations
  - Compares values against clinical reference ranges
  - Classifies parameters as Normal, High, or Low

- **📊 Health Summary Dashboard**
  - Overall Health Score (0-100)
  - Risk Level Assessment
  - Key Findings & Positive Indicators
  - Areas of Concern
  - Interactive parameter analysis

- **🥗 Personalized Diet Recommendations**
  - Foods to Include
  - Foods to Limit
  - Hydration Recommendations
  - Nutritional Suggestions
  - Condition-specific guidance

- **⚠️ Health Precautions Engine**
  - Daily Precautions
  - Lifestyle Changes
  - Monitoring Recommendations
  - Medical Follow-Up Suggestions

- **💬 Chat with Report**
  - Conversational healthcare assistant
  - Context-aware responses using report data
  - Conversation memory
  - Ask questions like:
    - "What does cholesterol mean?"
    - "Why is my glucose high?"
    - "What foods should I avoid?"
    - "Explain my report simply"

- **📥 Report Summary Download**
  - Generate downloadable text summary
  - Includes all analysis and recommendations

## 🏗️ Architecture

### Technology Stack

- **Frontend**: Streamlit (Interactive web UI)
- **Backend**: Python with LangChain
- **LLM**: Google Gemini API (gemini-2.5-flash)
- **Text Extraction**: pdfplumber, PyPDF2, EasyOCR
- **Data Storage**: Session-based (in-memory only, no databases)

### Project Structure

```
MediDrishtiAI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules
│
├── backend/                        # Backend modules
│   ├── __init__.py
│   ├── analyzer.py                # Parameter analysis logic
│   ├── chatbot.py                 # Conversational AI assistant
│   ├── diet_engine.py             # Diet recommendation logic
│   ├── health_score.py            # Health score calculation
│   ├── precaution_engine.py       # Precaution recommendation logic
│   ├── prompts.py                 # LangChain prompts
│   └── report_parser.py           # Report text extraction & parsing
│
├── frontend/                       # UI components
│   ├── __init__.py
│   └── ui.py                      # Streamlit UI utilities
│
├── utils/                          # Utility functions
│   └── __init__.py
│
├── assets/                         # Static assets
│   └── style.css                  # Custom styling
│
└── tests/                          # Test suite
    └── __init__.py
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API Key (get from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Step 1: Clone/Download the Project

```bash
cd MediDrishtiAI
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   Get your API key from: https://aistudio.google.com/app/apikey

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload Medical Report

- Navigate to "Upload Report" page
- Upload a PDF or image file of your medical report
- The system automatically extracts text and analyzes parameters

### 2. View Analysis Dashboard

- See your Health Score and Risk Level
- Review detailed parameter analysis
- Understand medical explanations and simple interpretations

### 3. Get Diet Recommendations

- View personalized foods to include/limit
- Get hydration and nutritional guidance
- Recommendations are tailored to your health parameters

### 4. Review Health Precautions

- Daily precautions for better health
- Lifestyle changes recommendations
- Health monitoring tips
- Medical follow-up suggestions

### 5. Chat with Report

- Ask questions about your report
- Get clarifications on medical terms
- Receive guidance on foods and lifestyle

### 6. Download Summary

- Generate a comprehensive text summary
- Download for personal records or sharing with healthcare providers

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
GOOGLE_API_KEY=your_api_key_here
```

### Customization

#### Change LLM Model

Edit `backend/chatbot.py` to use a different Google Generative AI model:
```python
model_name: str = "gemini-pro"  # or "gemini-2.5-flash"
```

#### Modify Reference Ranges

Update `backend/analyzer.py` REFERENCE_RANGES dictionary to adjust parameter ranges based on your region or lab standards.

#### Add Custom Recommendations

Edit `backend/diet_engine.py` and `backend/precaution_engine.py` to add condition-specific recommendations.

## 🔒 Security & Privacy

- ✅ **No Permanent Storage**: Reports are stored in session memory only
- ✅ **No Databases**: All data is processed in-memory during the session
- ✅ **API Key Security**: Stored in environment variables, never in code
- ✅ **Session Isolation**: Each user gets isolated session data
- ✅ **File Validation**: Strict file type validation
- ✅ **No External Sharing**: Data doesn't leave your session

## ⚙️ LangChain Integration

The application uses LangChain for:

- **PromptTemplate**: Structured prompt formatting
- **ChatPromptTemplate**: Multi-message conversation templates
- **ConversationBufferMemory**: Maintains chat history
- **LLMChain**: Chains prompts and LLM calls
- **StructuredOutputParser**: Parses LLM responses into structured format

## 🧪 Testing

Run tests with:

```bash
pytest tests/
```

## 📦 Deployment

### Streamlit Cloud Deployment

1. Push code to GitHub repository
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository and branch
5. Set environment variables in deployment settings:
   - `GOOGLE_API_KEY`: Your Gemini API key
6. Deploy

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GOOGLE_API_KEY=your_key_here

CMD ["streamlit", "run", "app.py"]
```

Build and run:

```bash
docker build -t medidristi-ai .
docker run -p 8501:8501 medidristi-ai
```

## 📋 API Reference

### Backend Modules

#### `report_parser.py`
- `validate_report_file(filename)`: Validates file type
- `extract_report_text(uploaded_file)`: Extracts text from reports
- `parse_medical_parameters(text)`: Extracts parameter values from text

#### `analyzer.py`
- `analyze_parameters(parsed_values)`: Analyzes each parameter
- `generate_health_summary(parameter_results)`: Creates health overview

#### `chatbot.py`
- `ReportChatAssistant`: Main chat interface
  - `ask(user_input)`: Get response from assistant

#### `diet_engine.py`
- `generate_diet_recommendations(parameter_results)`: Gets diet guidance

#### `precaution_engine.py`
- `generate_precaution_plan(parameter_results)`: Gets precautions

#### `health_score.py`
- `calculate_health_score(parameter_results)`: Computes health score
- `risk_level(score)`: Determines risk level

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not set"

**Solution**: Make sure `.env` file exists and contains your API key:
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### "ModuleNotFoundError" for langchain_google_genai

**Solution**: Install the package:
```bash
pip install langchain-google-genai
```

### "EasyOCR not installed"

**Solution**: Install it:
```bash
pip install easyocr
```

### Report text not extracted

**Solution**: 
- Verify PDF is valid
- Try a different PDF tool: pdfplumber is used first, then PyPDF2
- For images, ensure EasyOCR is installed

### Chat responses are slow

**Solution**: 
- Gemini API calls may take time depending on internet
- Session network issues can slow responses
- Try again with shorter questions

## 📝 Sample Medical Parameters

The system recognizes and analyzes:

- **Blood Parameters**: Hemoglobin, RBC, WBC, Platelets
- **Metabolic**: Blood Sugar, Cholesterol, Creatinine, Urea
- **Vitamins**: Vitamin D
- **Liver Enzymes**: AST, ALT, ALP, Bilirubin
- **And many more...**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and healthcare purposes.

## ⚠️ Medical Disclaimer

**Important**: MediDrishti AI is an educational tool and does NOT replace professional medical advice. Always consult with qualified healthcare professionals for medical decisions.

- 🚨 Results are AI-generated and may not be 100% accurate
- 🏥 For serious health concerns, see a doctor immediately
- 📋 Use this tool to understand reports, not to diagnose conditions
- 💊 Never change medications based solely on this analysis

## 🆘 Support

For issues, questions, or suggestions:

1. Check the Troubleshooting section
2. Review the code documentation
3. Check that all dependencies are installed
4. Ensure your Gemini API key is valid

## 🎓 Learning Resources

- [LangChain Documentation](https://docs.langchain.com)
- [Google Gemini API Docs](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Medical Reference Ranges](https://www.ncbi.nlm.nih.gov/)

## 📞 Version Information

- **Version**: 1.0.0
- **Last Updated**: June 2026
- **Python**: 3.8+
- **Streamlit**: 1.28+
- **LangChain**: 0.1+
- **Gemini API**: Latest

---

**Built with ❤️ for better healthcare understanding**
