# MediDrishti AI - Contributing Guide

Thank you for your interest in contributing to MediDrishti AI! This guide will help you understand how to contribute effectively.

## Code of Conduct

- Be respectful and inclusive
- Focus on code quality and clarity
- Help others learn and grow
- Report security issues privately

## Getting Started

### 1. Fork the Repository

```bash
# Create a fork on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/MediDrishtiAI.git
cd MediDrishtiAI
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install dependencies + dev tools
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Code Style

We follow PEP 8 with tools for consistency:

#### Format Code
```bash
black backend/ frontend/ app.py
```

#### Check Linting
```bash
flake8 backend/ frontend/ app.py
```

#### Type Checking
```bash
mypy backend/ frontend/ app.py
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/

# Run specific test
pytest tests/test_backend.py::TestAnalyzer::test_analyze_parameters_normal
```

### Before Committing

```bash
# 1. Format code
black .

# 2. Check linting
flake8 .

# 3. Run tests
pytest tests/

# 4. Check types
mypy .

# 5. Commit
git add .
git commit -m "Clear description of changes"
```

## Areas for Contribution

### 1. Core Features

#### Medical Parameters
- Add new medical parameters to `PARAMETER_PATTERNS`
- Add reference ranges to `REFERENCE_RANGES`
- Add explanations to `EXPLANATIONS`

**Files**: `backend/analyzer.py`, `backend/report_parser.py`

```python
# Example: Add new parameter
PARAMETER_PATTERNS = {
    "new_parameter": r"pattern_to_match",
}

REFERENCE_RANGES = {
    "new_parameter": {
        "normal": (min_value, max_value),
        "unit": "measurement_unit"
    }
}
```

#### Diet Recommendations
- Add new condition-based recommendations
- Improve existing recommendations
- Add region-specific food options

**File**: `backend/diet_engine.py`

#### Health Precautions
- Add new precaution categories
- Improve medical follow-up suggestions
- Add lifestyle-specific guidance

**File**: `backend/precaution_engine.py`

#### Chatbot Improvements
- Improve prompt templates
- Add conversation examples
- Enhance context handling

**Files**: `backend/chatbot.py`, `backend/prompts.py`

### 2. UI/UX Enhancements

- Improve Streamlit components
- Add new visualization features
- Enhance mobile responsiveness
- Improve accessibility

**Files**: `frontend/ui.py`, `assets/style.css`, `app.py`

### 3. Text Extraction

- Improve PDF parsing accuracy
- Enhance OCR performance
- Add support for new file formats
- Better error handling

**File**: `backend/report_parser.py`

### 4. Testing

- Add more unit tests
- Add integration tests
- Add edge case tests
- Improve test coverage

**File**: `tests/test_backend.py`

### 5. Documentation

- Improve existing documentation
- Add examples and use cases
- Create video tutorials
- Translate documentation

**Files**: `README.md`, `ARCHITECTURE.md`, `QUICKSTART.md`, etc.

## Making Changes

### Add a New Medical Parameter

1. **Update pattern matching** in `backend/report_parser.py`:
```python
PARAMETER_PATTERNS = {
    "parameter_name": r"regex_pattern_to_match"
}
```

2. **Add reference range** in `backend/analyzer.py`:
```python
REFERENCE_RANGES = {
    "parameter_name": {
        "normal": (min, max),
        "unit": "unit_of_measurement"
    }
}
```

3. **Add explanation** in `backend/analyzer.py`:
```python
EXPLANATIONS = {
    "parameter_name": {
        "normal": "Explanation when normal",
        "high": "Explanation when high",
        "low": "Explanation when low"
    }
}
```

4. **Add diet recommendation** in `backend/diet_engine.py`:
```python
CONDITION_RECOMMENDATIONS = {
    "parameter_name_status": {
        "include": ["food1", "food2"],
        "limit": ["food3", "food4"],
        "hydration": ["tip1"],
        "nutrition": ["tip2"]
    }
}
```

5. **Add precautions** in `backend/precaution_engine.py`:
```python
# In generate_precaution_plan function
if "parameter_name" in name:
    lifestyle.append("Lifestyle recommendation")
    monitoring.append("Monitoring tip")
    follow_up.append("Doctor consultation")
```

6. **Write tests** in `tests/test_backend.py`:
```python
def test_parse_parameter_name():
    text = "Parameter Name: 123 unit"
    result = parse_medical_parameters(text)
    assert "parameter_name" in result
```

### Improve Chatbot Prompts

Edit `backend/prompts.py`:

```python
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "Your improved system message here"
        ),
        HumanMessagePromptTemplate.from_template(
            "Your improved human message template"
        ),
    ]
)
```

### Add UI Component

Create new function in `frontend/ui.py`:

```python
def render_custom_component(title: str, data: dict) -> None:
    st.markdown(
        f"""
        <div class='custom-component'>
            <h3>{title}</h3>
            <!-- Your HTML here -->
        </div>
        """,
        unsafe_allow_html=True
    )
```

## Commit Guidelines

Write clear, concise commit messages:

```bash
# Good
git commit -m "Add insulin resistance parameter detection"
git commit -m "Fix PDF extraction for scanned documents"
git commit -m "Improve chat context handling"

# Avoid
git commit -m "Fix stuff"
git commit -m "Update file"
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/updates
- `perf`: Performance improvements

**Example**:
```
feat: Add thyroid parameter detection

Adds support for TSH and free T4 parameters
with proper reference ranges and diet guidance.

Fixes #123
```

## Pull Request Process

### Before Submitting

1. **Ensure code quality**:
   ```bash
   black .
   flake8 .
   mypy .
   pytest tests/
   ```

2. **Update documentation**:
   - Update README if needed
   - Add/update docstrings
   - Document API changes

3. **Test thoroughly**:
   - Test with various inputs
   - Test edge cases
   - Verify existing functionality still works

### Submit PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature
   ```

2. **Create Pull Request**:
   - Clear title and description
   - Link related issues: `Fixes #123`
   - Describe changes and testing
   - Include screenshots for UI changes

3. **PR Description Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] New feature
   - [ ] Bug fix
   - [ ] Documentation
   - [ ] Performance

   ## Testing
   Describe testing performed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No breaking changes
   ```

### Addressing Feedback

- Make requested changes
- Reply to comments
- Push updates: `git push`
- PR updates automatically

## Testing Requirements

### Unit Tests

Write tests for new functionality:

```python
def test_new_feature():
    # Arrange
    input_data = "test_input"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Test Coverage

Target 80%+ coverage:

```bash
pytest --cov=backend --cov-report=html tests/
```

### Integration Tests

Test complete workflows:

```python
def test_complete_report_analysis():
    # Upload → Parse → Analyze → Recommend
    # Verify all modules work together
    pass
```

## Documentation Standards

### Docstrings

Use Google-style docstrings:

```python
def analyze_parameters(parsed_values: dict) -> List[dict]:
    """Analyze medical parameters against reference ranges.
    
    Compares each parameter value to normal ranges and 
    generates medical and simple explanations.
    
    Args:
        parsed_values: Dictionary of parameter name to value
        
    Returns:
        List of analysis results with status and explanations
        
    Raises:
        ValueError: If parsed_values is empty
        
    Example:
        >>> result = analyze_parameters({"hemoglobin": "14.5"})
        >>> result[0]["status"]
        "Normal"
    """
```

### Comments

Add comments for complex logic:

```python
# Skip this parameter if it's not in reference ranges
if name not in REFERENCE_RANGES:
    continue
```

### README Updates

Update README.md when:
- Adding new features
- Changing installation steps
- Adding new dependencies
- Changing configuration

## Security Considerations

### API Keys
- Never commit API keys
- Use environment variables
- Never log sensitive data

### File Uploads
- Validate file types
- Check file size
- Sanitize filenames
- Clear files after processing

### Input Validation
- Validate all user inputs
- Prevent injection attacks
- Handle edge cases

## Performance Guidelines

- Use caching for expensive operations
- Avoid unnecessary API calls
- Optimize text processing
- Monitor memory usage

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Environment info

### Feature Requests

Include:
- Clear description
- Use case/motivation
- Proposed solution (optional)
- Examples/mockups (optional)

## Communication

- Ask questions in issues
- Discuss major changes before implementing
- Be patient and respectful
- Help others in discussions

## Review Process

### What We Look For

✅ **Good PR**:
- Clear, focused changes
- Thorough testing
- Updated documentation
- Follows code style
- Includes helpful comments
- Addresses one issue

❌ **Problematic PR**:
- Multiple unrelated changes
- No tests
- Poor code quality
- Breaking changes without discussion
- Incomplete documentation

### Merge Criteria

- [ ] All tests pass
- [ ] Code review approved
- [ ] No conflicts
- [ ] Documentation updated
- [ ] Changes follow guidelines

## Recognition

Contributors are recognized in:
- Release notes
- CONTRIBUTORS.md file
- GitHub contributors page

## Resources

- **Python Docs**: https://docs.python.org/
- **Streamlit Docs**: https://docs.streamlit.io/
- **LangChain Docs**: https://docs.langchain.com/
- **Git Guide**: https://git-scm.com/doc
- **Medical Reference**: https://www.ncbi.nlm.nih.gov/

## Questions?

- Ask in GitHub issues
- Check existing discussions
- Review documentation

---

**Thank you for contributing! Together we're building better healthcare tools. ❤️**
