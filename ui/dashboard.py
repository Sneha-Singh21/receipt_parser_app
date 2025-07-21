def run_dashboard():
    import streamlit as st
    import os
    import sys
    import pandas as pd
    from io import BytesIO
    from fpdf import FPDF

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from backend.db import get_all_receipts, search_by_vendor, sort_by, delete_receipt

    st.title("📊 Receipt Analytics Dashboard")

    # 🔍 Search by vendor
    vendor_query = st.text_input("🔎 Search by Vendor Name")
    if vendor_query:
        search_results = search_by_vendor(vendor_query)
        if search_results:
            st.write("🔍 Search Results")
            st.dataframe(pd.DataFrame(search_results, columns=["ID", "Filename", "Vendor", "Date", "Amount", "Category"]))
        else:
            st.warning("No results found.")

    # 🧾 Get All Data
    all_data = pd.DataFrame(get_all_receipts(), columns=["ID", "Filename", "Vendor", "Date", "Amount", "Category"])
    all_data['Date'] = pd.to_datetime(all_data['Date'], errors='coerce')

    # 📅 Date range filter (Safe fallback if no dates)
    min_date, max_date = all_data['Date'].min(), all_data['Date'].max()
    if pd.isna(min_date) or pd.isna(max_date):
        st.warning("No valid dates found in data to filter.")
        date_range = None
    else:
        date_range = st.date_input("📅 Filter by Date Range", [min_date.date(), max_date.date()])

    # ↕️ Sort by dropdown
    sort_field = st.selectbox("Sort by", ["date", "amount", "vendor"])
    sort_order = st.radio("Order", ["ASC", "DESC"], horizontal=True)
    sorted_data = sort_by(sort_field, sort_order)

    df_sorted = pd.DataFrame(sorted_data, columns=["ID", "Filename", "Vendor", "Date", "Amount", "Category"])
    df_sorted['Date'] = pd.to_datetime(df_sorted['Date'], errors='coerce')

    # 🏷️ Category filter
    unique_categories = all_data["Category"].dropna().unique().tolist()
    selected_categories = st.multiselect("🏷️ Filter by Category", options=unique_categories, default=unique_categories)

    if selected_categories:
        df_sorted = df_sorted[df_sorted["Category"].isin(selected_categories)]
        all_data = all_data[all_data["Category"].isin(selected_categories)]

    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        df_sorted = df_sorted[(df_sorted['Date'] >= pd.to_datetime(start_date)) & (df_sorted['Date'] <= pd.to_datetime(end_date))]
        all_data = all_data[(all_data['Date'] >= pd.to_datetime(start_date)) & (all_data['Date'] <= pd.to_datetime(end_date))]

    st.markdown("### 📋 Sorted Receipt Table")

    if not df_sorted.empty:
        for index, row in df_sorted.iterrows():
            cols = st.columns([1, 2, 2, 2, 2, 2, 1])
            cols[0].write(row["ID"])
            cols[1].write(row["Filename"])
            cols[2].write(row["Vendor"])
            cols[3].write(row["Date"].strftime('%Y-%m-%d') if pd.notna(row["Date"]) else "—")
            cols[4].write(f"₹{row['Amount']}")
            cols[5].write(row["Category"])
            if cols[6].button("🗑️", key=f"delete_{row['ID']}"):
                delete_receipt(row["ID"])
                st.success(f"Deleted: {row['Filename']}")
                st.rerun()

        # 📤 Export Buttons
        st.markdown("### 📤 Export Filtered Data")
        csv = df_sorted.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "receipts.csv", "text/csv")

        json = df_sorted.to_json(orient="records", indent=2)
        st.download_button("⬇️ Download JSON", json, "receipts.json", "application/json")

        # 📝 PDF Summary
        st.markdown("### 📝 Generate PDF Summary")
        if st.button("📄 Download Summary PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Receipt Summary", ln=True, align="C")
            pdf.ln(10)

            for i, row in df_sorted.iterrows():
                line = f"{row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else '—'} | {row['Vendor']} | ₹{row['Amount']} | {row['Category']}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf_buffer = BytesIO()
            pdf.output(pdf_buffer)
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_buffer.getvalue(),
                file_name="receipt_summary.pdf",
                mime="application/pdf"
            )
    else:
        st.info("No receipts found.")

    # 📊 Summary stats
    if not all_data.empty:
        st.markdown("### 📈 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spend", f"₹{all_data['Amount'].sum():,.2f}")
        col2.metric("Average Spend", f"₹{all_data['Amount'].mean():,.2f}")
        col3.metric("Highest Spend", f"₹{all_data['Amount'].max():,.2f}")

        st.markdown("### 🏬 Top Vendors")
        vendor_counts = all_data["Vendor"].value_counts()
        st.bar_chart(vendor_counts)

        st.markdown("### 📆 Monthly Spending Trend")
        df_monthly = all_data.groupby(all_data['Date'].dt.to_period("M"))['Amount'].sum().reset_index()
        df_monthly['Date'] = df_monthly['Date'].astype(str)
        st.line_chart(df_monthly.set_index("Date"))
    else:
        st.info("Upload receipts to view analytics.")
