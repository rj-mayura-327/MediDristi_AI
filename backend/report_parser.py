import re
from io import BytesIO

import pdfplumber
from PyPDF2 import PdfReader

try:
    import easyocr
except ImportError:
    easyocr = None

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

PARAMETER_PATTERNS = {
    "hemoglobin": r"hemoglobin\s*[:\-]?\s*([\d\.]+)\s*(g/dl|gm/dl|g/L)?",
    "rbc": r"rbc\s*[:\-]?\s*([\d\.]+)\s*(10\^12|x10\^12|million|10\^6)?",
    "wbc": r"wbc\s*[:\-]?\s*([\d\.]+)\s*(10\^9|x10\^9|10\^3)?",
    "platelets": r"platelets\s*[:\-]?\s*([\d\.]+)\s*(10\^9|x10\^9|10\^3)?",
    "blood sugar": r"(?:blood sugar|glucose|fasting glucose|random glucose)\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|mmol/L)?",
    "cholesterol": r"cholesterol\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|mmol/L)?",
    "vitamin d": r"vitamin\s*d\s*[:\-]?\s*([\d\.]+)\s*(ng/ml|nmol/L)?",
    "creatinine": r"creatinine\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|umol/L)?",
    "ast": r"ast\s*[:\-]?\s*([\d\.]+)\s*(u/L|u/l)?",
    "alt": r"alt\s*[:\-]?\s*([\d\.]+)\s*(u/L|u/l)?",
    "alp": r"alp\s*[:\-]?\s*([\d\.]+)\s*(u/L|u/l)?",
    "bilirubin": r"bilirubin\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|umol/L)?",
    "urea": r"urea\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|mmol/L)?",
}

GENERIC_PARAMETER_PATTERNS = [
    r"([A-Za-z ]{2,20})\s*[:\-]?\s*([\d\.]+)\s*(mg/dl|mmol/L|g/dl|ng/ml|u/L|umol/L|%)?",
]


def validate_report_file(filename: str) -> bool:
    if not filename:
        return False
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = []
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text.append(page_text)
    except Exception:
        reader = PdfReader(BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text).strip()


def extract_text_from_image(file_bytes: bytes) -> str:
    if easyocr is None:
        raise ImportError(
            "EasyOCR is not installed. Install it to parse image-based medical reports."
        )

    reader = easyocr.Reader(["en"], gpu=False)
    image_data = BytesIO(file_bytes).getvalue()
    results = reader.readtext(image_data, detail=0, paragraph=True)
    return "\n".join(results).strip()


def extract_report_text(uploaded_file) -> str:
    raw_bytes = uploaded_file.read()
    suffix = uploaded_file.name.lower().split(".")[-1]
    if suffix == "pdf":
        return extract_text_from_pdf(raw_bytes)
    if suffix in {"png", "jpg", "jpeg"}:
        return extract_text_from_image(raw_bytes)
    raise ValueError("Unsupported file format for medical report extraction.")


def _normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", " ")


def _find_by_patterns(text: str) -> dict:
    extracted = {}
    lowered = text.lower()
    for key, pattern in PARAMETER_PATTERNS.items():
        match = re.search(pattern, lowered)
        if match:
            extracted[key] = match.group(1)
    if not extracted:
        for pattern in GENERIC_PARAMETER_PATTERNS:
            for match in re.finditer(pattern, lowered):
                name, value = match.group(1).strip().lower(), match.group(2)
                if name in {"hemoglobin", "rbc", "wbc", "platelets", "cholesterol", "creatinine", "bilirubin", "ast", "alt", "alp", "urea"}:
                    extracted[name] = value
    return extracted


def parse_medical_parameters(text: str) -> dict:
    extracted = _find_by_patterns(text)
    if not extracted and text:
        return {}

    normalized = {}
    for key, value in extracted.items():
        normalized[key] = value
    return normalized
