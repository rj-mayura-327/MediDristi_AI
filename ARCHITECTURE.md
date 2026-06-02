# MediDrishti AI - Architecture & Design Document

Comprehensive overview of the MediDrishti AI system architecture, design patterns, and data flow.

## System Overview

MediDrishti AI is a production-ready healthcare report analysis web application built with Streamlit, LangChain, and Google Gemini API.

### Core Design Principles

1. **No External Databases**: All data is session-based, processed in-memory only
2. **Privacy First**: No permanent file storage, no cloud data retention
3. **Modular Architecture**: Clean separation of concerns with independent modules
4. **LLM-Agnostic**: Easy to switch between different LLM providers
5. **User-Friendly**: Professional healthcare UI with clear, simple explanations

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI Layer                     │
│              (frontend/ui.py, app.py)                    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               Business Logic Layer                        │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │  Analyzer    │  Diet Engine │  Precaution  │         │
│  │  (Extract &  │  (Food & Nut │  Engine      │         │
│  │   Analyze    │   Guidance)  │  (Care Tips) │         │
│  └──────────────┴──────────────┴──────────────┘         │
│  ┌──────────────┬──────────────┐                         │
│  │ Health Score │ Chat (Mem &  │                         │
│  │ Calculation  │ LangChain)   │                         │
│  └──────────────┴──────────────┘                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            Data Processing Layer                         │
│  ┌──────────────────────────────────────────────┐       │
│  │  Report Parser (PDF/Image Text Extraction)   │       │
│  │  - pdfplumber (PDF)                          │       │
│  │  - PyPDF2 (PDF fallback)                     │       │
│  │  - EasyOCR (Image/OCR)                       │       │
│  └──────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────┐       │
│  │  Parameter Parsing & Extraction              │       │
│  │  - Regex pattern matching                    │       │
│  │  - Medical parameter recognition             │       │
│  └──────────────────────────────────────────────┘       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         External Services & APIs                        │
│  ┌──────────────────────────────────────────────┐       │
│  │    Google Gemini API (LangChain Integration) │       │
│  │    - Medical analysis enhancement            │       │
│  │    - Chat assistant                          │       │
│  │    - Natural language understanding          │       │
│  └──────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Session State Management                    │
│  (Streamlit st.session_state - In-Memory Storage)       │
│  - Uploaded files & report text                         │
│  - Parsed parameters                                    │
│  - Analysis results                                     │
│  - Health summaries                                     │
│  - Chat history & memory                                │
│  - Recommendations (diet & precautions)                 │
└─────────────────────────────────────────────────────────┘
```

## Module Structure

### 1. **app.py** - Main Application Entry Point

**Responsibility**: Orchestrates the entire application flow

**Key Functions**:
- `initialize_session()`: Sets up session state variables
- `build_report_summary()`: Creates downloadable summary
- `upload_page()`: Handles report upload and processing
- `dashboard_page()`: Displays analysis results
- `diet_page()`: Shows diet recommendations
- `precautions_page()`: Displays health precautions
- `chat_page()`: Chat interface
- `download_page()`: Summary download
- `main()`: Streamlit app configuration and routing

**Data Flow**:
```
User Upload → Validation → Text Extraction → Parameter Parsing → 
Analysis → Recommendations → Display → Download
```

### 2. **backend/report_parser.py** - Text Extraction & Parsing

**Responsibility**: Extract and parse medical data from reports

**Key Components**:

#### File Validation
```python
validate_report_file(filename: str) -> bool
```
- Validates file extensions
- Supported: PDF, PNG, JPG, JPEG

#### Text Extraction
```python
extract_report_text(uploaded_file) -> str
```
- Dispatches to appropriate extraction method
- Handles multiple PDF libraries
- Falls back between pdfplumber and PyPDF2
- Uses EasyOCR for images

#### Parameter Parsing
```python
parse_medical_parameters(text: str) -> dict
```
- Uses regex patterns to find parameters
- Recognizes medical terminology
- Extracts numeric values with units
- Supports variations in formatting

**Supported Parameters**:
- Blood: Hemoglobin, RBC, WBC, Platelets
- Metabolic: Blood Sugar, Cholesterol, Creatinine, Urea
- Vitamins: Vitamin D
- Liver: AST, ALT, ALP, Bilirubin
- Extensible to any medical parameter

### 3. **backend/analyzer.py** - Medical Analysis

**Responsibility**: Analyze parsed parameters and generate insights

**Reference Ranges** (from REFERENCE_RANGES):
```python
{
    "parameter_name": {
        "normal": (min, max),
        "unit": "measurement_unit"
    }
}
```

**Key Functions**:

#### Parameter Analysis
```python
analyze_parameters(parsed_values: dict) -> List[dict]
```
- Compares against reference ranges
- Classifies as: Normal, High, Low
- Generates explanations at two levels:
  1. **Medical Explanation**: Professional clinical language
  2. **Simple Explanation**: Patient-friendly language

**Output Format**:
```json
{
    "parameter": "Hemoglobin",
    "value": "12.5",
    "normal_range": "12.0 - 17.5 g/dL",
    "status": "Normal",
    "medical_explanation": "...",
    "simple_explanation": "..."
}
```

#### Health Summary Generation
```python
generate_health_summary(parameter_results: List[dict]) -> dict
```
- Aggregates all findings
- Highlights positive indicators
- Identifies concerns
- Returns structured summary

### 4. **backend/health_score.py** - Health Scoring

**Responsibility**: Calculate health metrics and risk assessment

**Algorithm**:
```
Base Score = 100
For each abnormal parameter:
    Score -= 10 (High or Low status)
    Score -= 5 (Borderline status)
Final Score = max(0, min(100, Score))
```

**Risk Level Mapping**:
- **Low Risk**: Score ≥ 80
- **Moderate Risk**: Score 60-79
- **High Risk**: Score < 60

**Key Functions**:
```python
calculate_health_score(parameter_results: List[dict]) -> int
risk_level(score: int) -> str
```

### 5. **backend/diet_engine.py** - Nutrition Recommendations

**Responsibility**: Generate personalized diet guidance

**Architecture**:

#### Condition-Based Recommendations
Each condition (low hemoglobin, high cholesterol, etc.) maps to:
```python
{
    "include": [foods to add],
    "limit": [foods to reduce],
    "hydration": [hydration tips],
    "nutrition": [nutritional advice]
}
```

**Algorithm**:
1. Start with DEFAULT_DIET
2. For each abnormal parameter:
   - Look up CONDITION_RECOMMENDATIONS
   - Merge with existing recommendations
3. Return deduplicated, sorted recommendations

**Supported Conditions**:
- Low Hemoglobin → Iron-rich foods
- High Cholesterol → Heart-healthy foods
- High Blood Sugar → Low-glycemic foods
- Low Vitamin D → Vitamin D sources
- Kidney Concerns → Controlled protein/sodium
- Liver Concerns → Antioxidant-rich foods

### 6. **backend/precaution_engine.py** - Health Precautions

**Responsibility**: Generate actionable health precautions

**Categories**:
1. **Daily Precautions**: Immediate actions (exercise, hydration)
2. **Lifestyle Changes**: Long-term habits
3. **Monitoring Recommendations**: What to track
4. **Medical Follow-Up**: When to see doctor

**Algorithm**:
1. Include default precautions
2. For each abnormal parameter:
   - Add specific precautions
   - Add monitoring tips
   - Add doctor consultation guidance
3. Remove duplicates while preserving order

### 7. **backend/chatbot.py** - Conversational AI

**Responsibility**: Provide conversational healthcare assistance

**Architecture**:

#### LLM Integration
```python
GeminiClient
├── create_llm()
└── Uses: langchain_google_genai.ChatGoogleGenerativeAI

ReportChatAssistant
├── __init__(report_context)
├── Memory: ConversationBufferMemory
├── Chain: LLMChain with prompts
└── ask(user_input) -> response
```

**Key Components**:
- **Memory**: Maintains chat history during session
- **Prompts**: System message + context injection
- **LLM**: Google Gemini with temperature 0.2 (deterministic)
- **Context**: Full report text for accurate responses

**Interaction Flow**:
```
User Input → Format with Context → LLM Processing → Response → Store in Memory
```

### 8. **backend/prompts.py** - LangChain Prompts

**Responsibility**: Define structured prompts for LLM interaction

**Components**:

#### Chat Prompt Template
```python
ChatPromptTemplate with:
- System Message: Define assistant role and behavior
- Human Message: Include report context + user input + history
```

#### Response Schemas & Parsers
- StructuredOutputParser for consistent LLM responses
- ResponseSchema definitions for validation

**Prompt Design Principles**:
- Clear role definition
- Context injection with report text
- Chat history for continuity
- Output format specification

### 9. **frontend/ui.py** - UI Components

**Responsibility**: Reusable Streamlit UI components

**Components**:

#### Styling
```python
load_styles()  # Load CSS from assets/style.css
```

#### Cards & Metrics
```python
render_metric_card(label, value, description)
render_health_score(score, risk_level)
```

#### Sections & Lists
```python
render_page_header(title, subtitle)
render_section(title)
render_list(title, items)
render_report_status(status_text)
```

**Styling Features**:
- Responsive grid layout
- Professional healthcare theme
- Accessibility compliance
- Animation support
- Dark mode support

## Data Flow Diagrams

### Complete Report Analysis Flow

```
┌──────────────────────┐
│  Upload Medical      │
│  Report (PDF/Image)  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Validate File Type  │
│  (PDF/PNG/JPG/JPEG)  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Extract Text        │
│  - pdfplumber        │
│  - PyPDF2            │
│  - EasyOCR (images)  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Parse Parameters    │
│  Using Regex &       │
│  Pattern Matching    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Analyze Each        │
│  Parameter Against   │
│  Reference Ranges    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Calculate Health    │
│  Score & Risk Level  │
└──────────┬───────────┘
           │
           ▼
   ┌───────┴────────┐
   │                │
   ▼                ▼
┌─────────┐    ┌──────────────┐
│  Diet   │    │ Precautions  │
│ Recom.  │    │ Recom.       │
└────┬────┘    └──────┬───────┘
     │                │
     └────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │  Display on     │
    │  Dashboard      │
    └─────────────────┘
```

### Chat Flow

```
User Question
      │
      ▼
Format with Context:
- Report text
- Chat history
- User input
      │
      ▼
Send to Gemini LLM
      │
      ▼
LLM Processes:
- Understands medical context
- Refers to report data
- Maintains conversation continuity
      │
      ▼
Response Generated
      │
      ▼
Store in Memory
(ConversationBufferMemory)
      │
      ▼
Display to User
```

## Session State Management

Streamlit `st.session_state` manages all session data:

```python
{
    "uploaded_file": str,              # Filename
    "report_text": str,                # Full extracted text
    "parameters": dict,                # Parsed parameters
    "analysis_results": List[dict],    # Analyzed parameters
    "health_summary": dict,            # Health overview
    "diet_recommendations": dict,      # Diet guidance
    "precaution_plan": dict,          # Health precautions
    "chat_assistant": Object,         # Chat instance
    "summary_text": str               # Summary for download
}
```

**Lifecycle**:
1. Initialize on app start
2. Update on report upload
3. Persist during session
4. Clear on browser refresh/close

## External Dependencies

### Core Libraries
- **Streamlit**: Web UI framework
- **LangChain**: LLM orchestration
- **langchain_google_genai**: Gemini integration
- **pdfplumber**: PDF text extraction
- **PyPDF2**: PDF fallback extraction
- **Pillow**: Image processing
- **EasyOCR**: Image OCR (optional)
- **OpenCV**: Image utilities
- **python-dotenv**: Environment variables

### API Dependencies
- **Google Gemini API**: LLM backend
- **API Key Required**: Set via GOOGLE_API_KEY

## Error Handling Strategy

### File Upload Errors
```python
try:
    extracted = extract_report_text(uploaded_file)
    if not extracted:
        st.warning("No text extracted")
except Exception as e:
    st.error(f"Upload failed: {e}")
```

### API Errors
```python
try:
    response = llm.invoke(...)
except Exception as e:
    return f"Error: {str(e)}"
```

### Parameter Parsing Errors
```python
def _parse_number(value: str) -> float:
    try:
        return float(cleaned_value)
    except ValueError:
        return 0.0
```

## Performance Considerations

### Optimization Techniques
1. **Caching**: Streamlit's built-in caching for expensive operations
2. **Session Storage**: In-memory (fast, no DB overhead)
3. **Lazy Loading**: Only process when needed
4. **Reasonable Timeouts**: 30-60 second limits on API calls

### Scalability
- **Session-Based**: Each user has isolated session
- **No Database**: No bottlenecks from database queries
- **Stateless LLM**: Each API call independent
- **File Size Limits**: Max 50MB for uploads

## Security Architecture

### Data Protection
1. **In-Memory Only**: No permanent storage
2. **Session Isolation**: Each user separate state
3. **No External Sharing**: Data never leaves session
4. **API Key Security**: Environment variables only

### Input Validation
1. **File Type Validation**: Strict extension checks
2. **Size Limits**: Maximum file size checks
3. **Text Sanitization**: Remove potentially harmful content
4. **API Timeout**: Prevent hanging requests

## Extension Points

### Adding New Parameters
Edit `backend/analyzer.py`:
```python
PARAMETER_PATTERNS = {
    "new_parameter": r"pattern_to_match"
}

REFERENCE_RANGES = {
    "new_parameter": {"normal": (min, max), "unit": "unit"}
}
```

### Adding New Conditions
Edit `backend/diet_engine.py` and `backend/precaution_engine.py`:
```python
CONDITION_RECOMMENDATIONS = {
    "condition_name": {
        "include": [...],
        "limit": [...],
        ...
    }
}
```

### Switching LLM Providers
Edit `backend/chatbot.py`:
```python
# Change from ChatGoogleGenerativeAI to other LLM
from langchain_openai import ChatOpenAI
# Or use any LangChain-compatible LLM
```

---

**Last Updated**: June 2026
