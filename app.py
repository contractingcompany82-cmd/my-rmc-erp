import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- PDF GENERATOR CLASS ---
class ProfessionalSalarySlip(FPDF):
    def header(self):
        # Company Name & Header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, st.session_state.comp_name.upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Registered Office: Industrial Area, Phase-II, New Delhi-110020', 0, 1, 'C')
        self.cell(0, 5, f"GSTIN: {st.session_state.comp_gst}", 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32)

    def generate_slip(self, d):
        self.add_page()
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP FOR THE MONTH OF {d['month'].upper()}", 1, 1, 'C')
        
        # Employee Details Table
        self.set_font('Arial', 'B', 10)
        h = 7 # row height
        self.cell(45, h, "Employee Name", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['name'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Employee ID", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['id'], 1, 1)
        
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Designation", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['desig'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Department", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['dept'], 1, 1)
        
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Bank A/c No", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['bank'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Payment Mode", 1); self.set_font('Arial', '', 10); self.cell(50, h, "BANK TRANSFER", 1, 1)

        self.ln(10)

        # Earnings & Deductions Table
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(240, 240, 240)
        self.cell(60, h, "EARNINGS", 1, 0, 'C', True)
        self.cell(35, h, "AMOUNT", 1, 0, 'C', True)
        self.cell(60, h, "DEDUCTIONS", 1, 0, 'C', True)
        self.cell(35, h, "AMOUNT", 1, 1, 'C', True)

        self.set_font('Arial', '', 10)
        # Row 1
        self.cell(60, h, "Basic Salary", 1); self.cell(35, h, f"{d['basic']:.2f}", 1, 0, 'R')
        self.cell(60, h, "PF Contribution", 1); self.cell(35, h, f"{d['pf']:.2f}", 1, 1, 'R')
        # Row 2
        self.cell(60, h, "HRA / Allowances", 1); self.cell(35, h, f"{d['allowance']:.2f}", 1, 0, 'R')
        self.cell(60, h, "ESIC / Medical", 1); self.cell(35, h, f"{d['esic']:.2f}", 1, 1, 'R')
        # Row 3
        self.cell(60, h, "Special Pay", 1); self.cell(35, h, f"{d['special']:.2f}", 1, 0, 'R')
        self.cell(60, h, "Professional Tax", 1); self.cell(35, h, f"{d['ptax']:.2f}", 1, 1, 'R')
        # Row 4
        self.cell(60, h, "Incentive / GST Benefit", 1); self.cell(35, h, f"{d['gst_bonus']:.2f}", 1, 0, 'R')
        self.cell(60, h, "TDS / Income Tax", 1); self.cell(35, h, f"{d['tds']:.2f}", 1, 1, 'R')

        # Totals
        self.set_font('Arial', 'B', 10)
        gross = d['basic'] + d['allowance'] + d['special'] + d['gst_bonus']
        total_ded = d['pf'] + d['esic'] + d['ptax'] + d['tds']
        net = gross - total_ded

        self.cell(60, h, "GROSS EARNINGS", 1); self.cell(35, h, f"{gross:.2f}", 1, 0, 'R')
        self.cell(60, h, "TOTAL DEDUCTIONS", 1); self.cell(35, h, f"{total_ded:.2f}", 1, 1, 'R')

        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.cell(190, 12, f"NET PAYABLE (In-Hand): Rs. {net:,.2f}", 1, 1, 'C', True)

        self.ln(20)
        self.set_font('Arial', 'I', 8)
        self.cell(95, 5, "_______________________", 0, 0, 'C')
        self.cell(95, 5, "_______________________", 0, 1, 'C')
        self.cell(95, 5, "Employee Signature", 0, 0, 'C')
        self.cell(95, 5, "Authorized Signatory", 0, 1, 'C')

# --- STREAMLIT UI ---
st.title("🏛️ Corporate Salary ERP System")

# Company Settings in Sidebar
with st.sidebar:
    st.header("Company Settings")
    st.session_state.comp_name = st.text_input("Company Name", "Global RMC Private Limited")
    st.session_state.comp_gst = st.text_input("Company GSTIN", "07AAAAA0000A1Z5")

# 1. Employee Info
c1, c2 = st.columns(2)
with c1:
    e_name = st.text_input("Name", "Rahul Sharma")
    e_id = st.text_input("ID", "EMP/RMC/052")
    e_dept = st.text_input("Dept", "Plant Operations")
    e_bank = st.text_input("Bank A/c", "XXXXXXXX4567")

with c2:
    e_desig = st.text_input("Designation", "Senior Engineer")
    month = st.selectbox("Month", ["January 2026", "February 2026", "March 2026"])

st.divider()

# 2. Financials
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Earnings")
    basic = st.number_input("Basic Salary", value=30000)
    allowance = st.number_input("HRA / Allowances", value=10000)
    special = st.number_input("Special / Bonus", value=2000)
    gst_bonus = st.number_input("GST/Incentive Benefit", value=0)

with col_b:
    st.subheader("Deductions")
    pf = st.number_input("PF Deduction", value=1800)
    esic = st.number_input("ESIC Deduction", value=500)
    ptax = st.number_input("Professional Tax", value=200)
    tds = st.number_input("TDS / Income Tax", value=0)

# 3. Generate
if st.button("Generate Professional Salary Slip"):
    data = {
        'name': e_name, 'id': e_id, 'dept': e_dept, 'bank': e_bank,
        'desig': e_desig, 'month': month, 'basic': basic, 
        'allowance': allowance, 'special': special, 'gst_bonus': gst_bonus,
        'pf': pf, 'esic': esic, 'ptax': ptax, 'tds': tds
    }
    
    pdf = ProfessionalSalarySlip()
    pdf.generate_slip(data)
    
    # Save & Download
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button(
        label="📥 Download Professional PDF Slip",
        data=pdf_bytes,
        file_name=f"SalarySlip_{e_name}.pdf",
        mime="application/pdf"
    )
    st.success("Professional Slip Generated Successfully!")
