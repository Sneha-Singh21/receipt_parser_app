# 🧾 Receipt Parser App

A powerful, interactive web application built using **Python + Streamlit** to extract and manage receipt data from uploaded images, PDFs, and text files. The app leverages OCR (Tesseract), PDF and text parsing, and integrates with a local **SQLite database** for storage and analytics.

---

## 🚀 Features Implemented

### ✅ STAGE 1: Upload Interface
- Upload files: `.jpg`, `.png`, `.pdf`, `.txt`
- Upload ZIP files to parse multiple receipts at once
- Prevent duplicate uploads
- Save all uploaded files to `data/uploads/`

### ✅ STAGE 2: Data Extraction
- Use **Tesseract OCR** to extract text from images (`.jpg`, `.png`)
- Use **pdfplumber** to read and extract text from PDF files
- Handle `.txt` files using standard text read
- Automatically parse: **Vendor**, **Date**, **Amount**, and **Category**

### ✅ STAGE 3: Database Integration
- Save parsed data into **SQLite** using `sqlite3`
- Store fields: `Filename`, `Vendor`, `Date`, `Amount`, `Category`
- Prevent insertion of duplicate files

### ✅ STAGE 4: Dashboard & Analytics
- View all saved receipts in a sortable, searchable table
- Search by vendor
- Filter by:
  - Date range
  - Category (multiselect)
- Sort data by:
  - Date
  - Amount
  - Vendor
- Inline preview of:
  - `.jpg`, `.png` (via `st.image`)
  - `.pdf` files (via iframe)
- Export data to:
  - CSV
  - JSON
- Generate a PDF summary report
- Delete individual receipts from UI & DB
- Summary Metrics:
  - Total Spend
  - Average Spend
  - Highest Spend
- Charts:
  - Monthly spending trend (Line Chart)
  - Top Vendors (Bar Chart)


## 📁 Project Structure

receipt_parser_app/
├── backend/
│ ├── db.py # SQLite DB logic
│ ├── parser.py # OCR + parsing utilities
│ └── utils.py # File type validation
│
├── ui/
│ ├── app.py # Main Streamlit App (Navigation + Uploads)
│ └── dashboard.py # Dashboard UI and Analytics
│
├── data/
│ └── uploads/ # Stores uploaded receipt files
│
└── requirements.txt # Python dependencies


## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/receipt-parser-app.git
cd receipt-parser-app/ui
2️⃣ Install Python Packages

pip install -r ../requirements.txt
3️⃣ Install Tesseract OCR
Download and install Tesseract from:
👉 https://github.com/UB-Mannheim/tesseract/wiki

After installing, add tesseract.exe path to system environment variables (e.g. C:\Program Files\Tesseract-OCR\).

4️⃣ Run the App

streamlit run app.py
📌 Notes
Compatible with Python 3.8+

Tested on Windows environment with Tesseract v5.x

Ensure PDF/image quality is good for accurate OCR

🙋‍♀️ Author
Sneha Singh
Final Year B.Tech CSE Student
Aspiring Full-Stack Developer & Data Analyst

📄 License
This project is for educational and internship evaluation purposes only.