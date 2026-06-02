# MediDrishti AI - Configuration Guide

Comprehensive guide for configuring MediDrishti AI for different environments and use cases.

## Environment Variables

### Required Variables

#### GOOGLE_API_KEY
Your Google Gemini API key for LLM functionality.

```bash
GOOGLE_API_KEY=your_api_key_here
```

**Get your key**: https://aistudio.google.com/app/apikey

### Optional Variables

#### Streamlit Configuration
```bash
# Server settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info

# Theme settings
STREAMLIT_THEME_BASE=light
STREAMLIT_THEME_PRIMARY_COLOR=#0066cc
STREAMLIT_THEME_BACKGROUND_COLOR=#f8f9fa
STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#ffffff
STREAMLIT_THEME_TEXT_COLOR=#1a1a1a
```

#### Application Settings
```bash
# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false

# Performance
MAX_FILE_SIZE_MB=50
REQUEST_TIMEOUT_SECONDS=60

# Feature Flags
ENABLE_OCRI=true
ENABLE_CHAT=true
ENABLE_DOWNLOAD=true
```

## File Configuration

### .env File Setup

**Location**: Project root directory

**Example** `.env`:
```env
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional - Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info

# Optional - Application
DEBUG_MODE=false
MAX_FILE_SIZE_MB=50
```

### streamlit/config.toml

Create `~/.streamlit/config.toml` for persistent Streamlit settings:

```toml
[theme]
base = "light"
primaryColor = "#0066cc"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#1a1a1a"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "viewer"
showSidebarNavigation = true

[logger]
level = "info"

[server]
maxUploadSize = 50
enableXsrfProtection = true
```

## Medical Reference Ranges

Customize reference ranges in `backend/analyzer.py`:

```python
REFERENCE_RANGES = {
    "hemoglobin": {
        "normal": (12.0, 17.5),  # Min, Max
        "unit": "g/dL"           # Unit of measurement
    },
    # Add more parameters...
}
```

### Adjusting for Your Region

Different labs use different ranges. Update values based on your local lab standards:

```python
# Example: If your lab uses different hemoglobin ranges
"hemoglobin": {
    "normal": (11.5, 18.0),  # Your lab's range
    "unit": "g/dL"
}
```

## Diet Recommendations Configuration

Customize diet guidance in `backend/diet_engine.py`:

```python
CONDITION_RECOMMENDATIONS = {
    "low hemoglobin": {
        "include": ["Spinach", "Dates", ...],
        "limit": ["Caffeine with meals", ...],
        "hydration": ["Water throughout the day", ...],
        "nutrition": ["Iron-rich foods", ...]
    },
    # Add more conditions...
}
```

### Adding New Conditions

```python
"new_condition": {
    "include": [
        "Food 1",
        "Food 2",
        "Food 3"
    ],
    "limit": [
        "Food to avoid 1",
        "Food to avoid 2"
    ],
    "hydration": [
        "Hydration tip 1",
        "Hydration tip 2"
    ],
    "nutrition": [
        "Nutritional advice 1",
        "Nutritional advice 2"
    ]
}
```

## LLM Model Configuration

### Changing the AI Model

Edit `backend/chatbot.py`:

```python
class GeminiClient:
    def __init__(
        self, 
        api_key: str = None, 
        model_name: str = "gemini-2.5-flash"  # Change this
    ):
        # ...
```

Available Google models:
- `gemini-2.5-flash`: Latest, fast, recommended
- `gemini-pro`: Older, more capable
- `gemini-pro-vision`: With vision support

### Adjusting Temperature

Lower = More deterministic, Higher = More creative

```python
return ChatGoogleGenerativeAI(
    model=self.model_name, 
    temperature=0.2,  # Change this (0.0-1.0)
    google_api_key=self.api_key,
)
```

### Switching to Different LLM Providers

#### Using OpenAI
```python
from langchain_openai import ChatOpenAI

def create_llm(self):
    return ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY")
    )
```

#### Using Anthropic Claude
```python
from langchain_anthropic import ChatAnthropic

def create_llm(self):
    return ChatAnthropic(
        model="claude-3-opus-20240229",
        temperature=0.2,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
```

#### Using Ollama (Local)
```python
from langchain_ollama import ChatOllama

def create_llm(self):
    return ChatOllama(
        model="mistral",
        base_url="http://localhost:11434"
    )
```

## UI Customization

### Styling

Edit `assets/style.css` to customize colors, fonts, and layout.

#### Color Theme
```css
:root {
    --primary-color: #0066cc;        /* Main brand color */
    --secondary-color: #00a86b;      /* Accent color */
    --warning-color: #ff6b35;        /* Warning alerts */
    --danger-color: #d62828;         /* Error alerts */
    --success-color: #06a77d;        /* Success alerts */
}
```

#### Font & Typography
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
```

### Custom Components

Add custom Streamlit components in `frontend/ui.py`:

```python
def render_custom_card(title: str, content: str) -> None:
    st.markdown(
        f"""
        <div class='custom-card'>
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
```

## Medical Explanation Configuration

Customize medical explanations in `backend/analyzer.py`:

```python
EXPLANATIONS = {
    "hemoglobin": {
        "normal": "Your custom normal explanation",
        "high": "Your custom high explanation",
        "low": "Your custom low explanation"
    },
    # Add more parameters...
}
```

## File Upload Configuration

### Maximum File Size

Edit `app.py`:

```python
uploaded_file = st.file_uploader(
    "Upload your medical report",
    type=list(ALLOWED_EXTENSIONS),
    accept_multiple_files=False,
)

# Note: Set server-wide max size in .streamlit/config.toml
# [server]
# maxUploadSize = 50  # MB
```

### Supported File Types

Edit `backend/report_parser.py`:

```python
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}  # Add more here
```

## Text Extraction Configuration

### PDF Extraction Priority

Edit `backend/report_parser.py`:

```python
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = []
    try:
        # Try pdfplumber first (recommended)
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
    except Exception:
        # Fallback to PyPDF2
        reader = PdfReader(BytesIO(file_bytes))
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text).strip()
```

### OCR Configuration

Edit `backend/report_parser.py`:

```python
def extract_text_from_image(file_bytes: bytes) -> str:
    reader = easyocr.Reader(
        ["en"],  # Languages
        gpu=False  # Set to True if you have GPU
    )
    # ...
```

## Health Score Thresholds

Adjust risk classifications in `backend/health_score.py`:

```python
RISK_THRESHOLDS = {
    "low": 80,       # Score >= 80 = Low risk
    "moderate": 60,  # Score >= 60 = Moderate risk
    "high": 40,      # Score < 60 = High risk
}
```

## Logging Configuration

### Streamlit Logging

Set in `.streamlit/config.toml`:

```toml
[logger]
level = "debug"  # debug, info, warning, error, critical
```

### Application Logging

Create `logging_config.py`:

```python
import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(
        'app.log',
        maxBytes=1000000,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
```

## Performance Tuning

### Caching

Add to `app.py`:

```python
@st.cache_data
def load_static_data():
    # Load once and cache
    return expensive_operation()

@st.cache_resource
def get_llm_instance():
    # Create once per session
    return GeminiClient().create_llm()
```

### Optimization Tips

1. **Use smaller PDFs**: Faster processing
2. **Reduce conversation history**: Clear chat if memory issues
3. **Increase timeout**: For slower connections
4. **Use specific regions**: Choose Gemini API nearest to you

## Multi-User Deployment

### Session Isolation

Each user automatically gets isolated session state through Streamlit.

### Concurrency Settings

For multiple concurrent users, adjust in `.streamlit/config.toml`:

```toml
[client]
maxMessageSize = 200

[server]
maxUploadSize = 50
enableXsrfProtection = true
```

## Analytics & Monitoring

### Adding Analytics

```python
import streamlit as st

# Track page views
def track_page_view(page_name):
    if "page_views" not in st.session_state:
        st.session_state.page_views = {}
    st.session_state.page_views[page_name] = \
        st.session_state.page_views.get(page_name, 0) + 1
```

### Monitoring Tools

- **Streamlit Cloud**: Built-in metrics dashboard
- **Sentry**: Error tracking
- **DataDog**: Application monitoring
- **Prometheus**: Metrics collection

## Troubleshooting Configuration Issues

### Issue: Settings Not Applied

**Solution**: Clear cache and restart
```bash
streamlit cache clear
streamlit run app.py
```

### Issue: API Key Not Found

**Solution**: Verify .env file exists and has correct format
```bash
cat .env  # macOS/Linux
type .env  # Windows
```

### Issue: Wrong File Extracted

**Solution**: Check file type and enable debug logging
```bash
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py
```

---

**Last Updated**: June 2026
