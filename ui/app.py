import streamlit as st
import os
import sys
import zipfile
import datetime
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.db import init_db, insert_receipt, get_all_receipts
from backend.utils import is_valid_filetype
from backend.parser import extract_text, extract_fields

UPLOAD_DIR = "data/uploads"
init_db()

# 🧭 Sidebar Navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["Upload Receipt", "Dashboard"])

if page == "Upload Receipt":
    st.title("🧾 Receipt Parser - Upload & Parse")

    # 📂 Upload ZIP of receipts
    st.markdown("### 📂 Upload Multiple Receipts (ZIP)")
    uploaded_zip = st.file_uploader("Upload ZIP file", type="zip")
    if uploaded_zip:
        summary_rows = []
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            extract_path = UPLOAD_DIR
            zip_ref.extractall(extract_path)
            st.success("✅ ZIP extracted and files uploaded!")

            existing_files = [r[1] for r in get_all_receipts()]

            for filename in zip_ref.namelist():
                filepath = os.path.join(extract_path, filename)
                if not is_valid_filetype(filename):
                    summary_rows.append({"Filename": filename, "Status": "❌ Invalid file type"})
                    continue

                if filename in existing_files:
                    summary_rows.append({"Filename": filename, "Status": "⚠️ Duplicate - Skipped"})
                    continue

                try:
                    extracted_text = extract_text(filepath)
                    parsed_data = extract_fields(extracted_text)

                    insert_receipt(
                        filename=filename,
                        vendor=parsed_data.get("vendor", ""),
                        date=parsed_data.get("date") or str(datetime.date.today()),
                        amount=parsed_data.get("amount") or 0.0,
                        category=parsed_data.get("category") or "Uncategorized"
                    )
                    summary_rows.append({"Filename": filename, "Status": "✅ Parsed & Saved"})
                except Exception as e:
                    summary_rows.append({"Filename": filename, "Status": f"❌ Error: {str(e)}"})

        # 📊 Show ZIP upload summary
        st.markdown("#### 📋 Upload Summary")
        st.dataframe(pd.DataFrame(summary_rows))

    uploaded_file = st.file_uploader("Upload a receipt (.jpg, .png, .pdf, .txt)", type=["jpg", "png", "pdf", "txt"])

    if uploaded_file:
        if is_valid_filetype(uploaded_file.name):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            filepath = os.path.join(UPLOAD_DIR, uploaded_file.name)

            existing_files = [r[1] for r in get_all_receipts()]
            if uploaded_file.name in existing_files:
                st.warning("⚠️ File already exists in the database. Please rename or upload a different file.")
            else:
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

                extracted_text = extract_text(filepath)
                st.subheader("📄 Extracted Text")
                st.code(extracted_text)

                # 👉 Extract structured fields
                parsed_data = extract_fields(extracted_text)
                st.subheader("✏️ Edit Parsed Fields Before Saving")

                # Editable form
                with st.form("edit_form"):
                    vendor = st.text_input("Vendor", parsed_data.get("vendor", ""))
                    date = st.date_input("Date", parsed_data.get("date") or datetime.date.today())
                    amount = st.number_input("Amount", value=parsed_data.get("amount") or 0.0)
                    category = st.text_input("Category", parsed_data.get("category") or "")

                    submit_btn = st.form_submit_button("Save to Database")

                if submit_btn:
                    insert_receipt(
                        filename=uploaded_file.name,
                        vendor=vendor,
                        date=str(date),
                        amount=amount,
                        category=category
                    )
                    st.success("✅ Updated data saved to database!")

        else:
            st.error("❌ Invalid file type. Allowed: jpg, png, pdf, txt.")

elif page == "Dashboard":
    # 🚀 Import and run dashboard content dynamically
    from dashboard import run_dashboard
    run_dashboard()
