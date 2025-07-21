import pytesseract
import pdfplumber
from PIL import Image
import os
import re
from datetime import datetime

# Set path to tesseract.exe (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Known vendor mappings for category
KNOWN_VENDORS = {
    "Reliance Jio": "Internet",
    "Amazon": "Shopping",
    "Big Bazaar": "Groceries",
    "Swiggy": "Food Delivery",
    "Flipkart": "Shopping"
}

# 🖼️ Extract text from image
def extract_text_from_image(filepath):
    try:
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[ERROR - image] {e}"

# 📄 Extract text from PDF
def extract_text_from_pdf(filepath):
    try:
        text = ''
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"[ERROR - pdf] {e}"

# 📝 Extract text from TXT
def extract_text_from_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR - txt] {e}"

# 🤖 Main text extractor
def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.jpg', '.png']:
        return extract_text_from_image(filepath)
    elif ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.txt':
        return extract_text_from_txt(filepath)
    else:
        return "[Unsupported file type]"

# 🧠 Extract structured fields: vendor, date, amount
def extract_fields(text):
    vendor = None
    date = None
    amount = None
    category = None

    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    # 🔍 Vendor: top 5 lines
    for line in lines[:5]:
        for known in KNOWN_VENDORS:
            if known.lower() in line.lower():
                vendor = known
                category = KNOWN_VENDORS[known]
                break
        if vendor:
            break
    if not vendor and lines:
        vendor = lines[0]

    # 🔍 Date
    date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b'
    date_match = re.search(date_pattern, text)
    if date_match:
        try:
            date = datetime.strptime(date_match.group(1), "%d-%m-%Y").date()
        except:
            try:
                date = datetime.strptime(date_match.group(1), "%d/%m/%Y").date()
            except:
                date = date_match.group(1)

    # 🔍 Amount
    amount_pattern = r'₹?\s?(\d+\.\d{2})'
    amount_match = re.search(amount_pattern, text)
    if amount_match:
        amount = float(amount_match.group(1))

    return {
        "vendor": vendor,
        "date": str(date) if date else None,
        "amount": amount,
        "category": category
    }
