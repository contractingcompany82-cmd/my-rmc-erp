import streamlit as st
from fpdf import FPDF
import pandas as pd

# Page Config
st.set_page_config(page_title="RMC Salary ERP", layout="wide")

# Error Handling for PDF
try:
    class SalaryPDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'RMC CONSTRUCTIONS ERP', 0, 1, 'C')
            self.line(10, 25, 200, 25)
            self.ln(10)

    # UI Start
    st.title("🏗️ Salary Slip Management System")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employee Details")
        emp_name = st.text_input("Name", "Amit Kumar")
        emp_id = st.text_input("ID", "RMC-101")
        dept = st.selectbox("Department", ["Production", "Sales", "Logistics", "Accounts"])
        month = st.selectbox("Month", ["January 2026", "February 2026", "March 2026"])

    with col2:
        st.subheader("Salary Components")
        basic = st.number_input("Basic Salary", value=20000)
        allowance = st.number_input("Allowances", value=5000)
        deduction = st.number_input("Deductions", value=1000)
        tax_pct = st.slider("Tax (%)", 0, 20, 5)

    # Calculations
    gross = basic + allowance
    tax_amt = (gross * tax_pct) / 100
    net = gross - deduction - tax_amt

    st.divider()

    # Calculation Preview
    st.subheader("Salary Summary")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Gross Salary", f"₹{gross}")
    res_col2.metric("Total Deductions", f"₹{deduction + tax_amt}")
    res_col3.metric("Net In-Hand", f"₹{net}", delta_color="normal")

    if st.button("Generate Professional PDF Slip"):
        pdf = SalaryPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        
        # Adding Data to PDF
        pdf.cell(0, 10, f"Salary Slip: {month}", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(95, 10, f"Employee: {emp_name}", border=1)
        pdf.cell(95, 10, f"ID: {emp_id}", border=1, ln=True)
        pdf.cell(95, 10, f"Dept: {dept}", border=1)
        pdf.cell(95, 10, f"Net Paid: RS. {net}", border=1, ln=True)
        
        # Export PDF
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="Click here to Download PDF",
            data=pdf_bytes,
            file_name=f"Slip_{emp_name}.pdf",
            mime="application/pdf"
        )
        st.success("PDF Ready for Download!")

except Exception as e:
    st.error(f"Ek panga ho gaya: {e}")
    st.info("Check karo requirements.txt mein 'fpdf' likha hai ya nahi.")
