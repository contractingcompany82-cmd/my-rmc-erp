import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- ADVANCED PDF CLASS (TABLE STYLE + WATERMARK + SIGN) ---
class ProfessionalSalarySlip(FPDF):
    def header(self):
        # Company Header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, st.session_state.get('comp_name', 'COMPANY NAME').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Registered Office: Industrial Area, New Delhi', 0, 1, 'C')
        self.cell(0, 5, f"GSTIN: {st.session_state.get('comp_gst', 'N/A')}", 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32)

    def add_watermark(self):
        # Company Name Watermark (Faint Gray)
        self.set_font('Arial', 'B', 50)
        self.set_text_color(245, 245, 245) 
        self.rotate(45, 100, 150)
        self.text(35, 190, st.session_state.get('comp_name', 'RMC ERP').upper())
        self.rotate(0)
        self.set_text_color(0, 0, 0)

    def generate_slip(self, d):
        self.add_page()
        self.add_watermark()
        self.ln(10)
        
        # Payslip Title Box
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f"PAYSLIP FOR THE MONTH OF {d['month'].upper()}", 1, 1, 'C', True)
        
        # 1. Employee Details Table (Pichle professional code jaisa)
        self.set_font('Arial', 'B', 10)
        h = 8 
        self.cell(45, h, "Employee Name", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['name'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Employee ID", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['id'], 1, 1)
        
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Designation", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['desig'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Department", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['dept'], 1, 1)
        
        self.ln(8)

        # 2. Earnings & Deductions Table (Side-by-Side Professional Layout)
        self.set_font('Arial', 'B', 10)
        self.cell(60, h, "EARNINGS", 1, 0, 'C', True)
        self.cell(35, h, "AMOUNT", 1, 0, 'C', True)
        self.cell(60, h, "DEDUCTIONS", 1, 0, 'C', True)
        self.cell(35, h, "AMOUNT", 1, 1, 'C', True)

        self.set_font('Arial', '', 10)
        # Row 1: Basic & PF
        self.cell(60, h, "Basic Salary", 1); self.cell(35, h, f"{d['basic']:.2f}", 1, 0, 'R')
        self.cell(60, h, "PF Contribution", 1); self.cell(35, h, f"{d['pf']:.2f}", 1, 1, 'R')
        # Row 2: HRA & ESIC/Tax
        self.cell(60, h, "HRA / Allowances", 1); self.cell(35, h, f"{d['allowance']:.2f}", 1, 0, 'R')
        self.cell(60, h, "TDS / Income Tax", 1); self.cell(35, h, f"{d['tds']:.2f}", 1, 1, 'R')
        # Row 3: Special & PT
        self.cell(60, h, "Special Pay", 1); self.cell(35, h, f"{d['special']:.2f}", 1, 0, 'R')
        self.cell(60, h, "Professional Tax", 1); self.cell(35, h, f"{d['ptax']:.2f}", 1, 1, 'R')

        # Totals
        self.set_font('Arial', 'B', 10)
        gross = d['basic'] + d['allowance'] + d['special']
        total_ded = d['pf'] + d['tds'] + d['ptax']
        net = gross - total_ded

        self.cell(60, h, "GROSS EARNINGS", 1); self.cell(35, h, f"{gross:.2f}", 1, 0, 'R')
        self.cell(60, h, "TOTAL DEDUCTION", 1); self.cell(35, h, f"{total_ded:.2f}", 1, 1, 'R')

        # Net Payable Highlight
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.cell(190, 12, f"NET PAYABLE (In-Hand): Rs. {net:,.2f}", 1, 1, 'C', True)

        # 3. DIGITAL SIGNATURE SEAL (Bottom Right)
        self.ln(25)
        self.set_draw_color(0, 102, 204) # Blue Border for Sign
        self.set_line_width(0.5)
        self.rect(130, 220, 60, 30) 
        
        self.set_xy(130, 222)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.cell(60, 5, "DIGITALLY SIGNED BY", 0, 1, 'C')
        self.set_font('Arial', 'B', 9)
        self.cell(60, 5, st.session_state.get('comp_name', 'COMPANY').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 7)
        self.cell(60, 5, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 0, 1, 'C')
        self.cell(60, 5, "Authentic ERP Document", 0, 1, 'C')
        self.set_text_color(0, 0, 0) # Reset

# --- STREAMLIT UI ---
st.title("🛡️ Professional Salary ERP v3.0")

with st.sidebar:
    st.header("🏢 Company Setup")
    st.session_state.comp_name = st.text_input("Company Name", "Global RMC Private Ltd")
    st.session_state.comp_gst = st.text_input("GSTIN", "07AAAAA0000A1Z5")

with st.form("salary_form"):
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Employee Info")
        name = st.text_input("Name", "Rahul Sharma")
        emp_id = st.text_input("ID", "EMP/RMC/102")
        dept = st.text_input("Department", "Operations")
        desig = st.text_input("Designation", "Plant Head")
        month = st.selectbox("Month", ["January 2026", "February 2026"])
    
    with c2:
        st.subheader("Salary Info")
        basic = st.number_input("Basic Salary", value=35000)
        allowance = st.number_input("HRA/Allowances", value=10000)
        special = st.number_input("Special Pay", value=2000)
        pf = st.number_input("PF Deduction", value=1800)
        tds = st.number_input("TDS/Tax", value=500)
        ptax = st.number_input("Prof. Tax", value=200)
    
    submit = st.form_submit_button("Preview & Generate PDF")

if submit:
    data = {
        'name': name, 'id': emp_id, 'dept': dept, 'desig': desig, 'month': month,
        'basic': basic, 'allowance': allowance, 'special': special,
        'pf': pf, 'tds': tds, 'ptax': ptax
    }
    
    pdf = ProfessionalSalarySlip()
    pdf.generate_slip(data)
    
    # Save PDF to Memory for Download
    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    st.download_button(
        label="📥 Download Digitally Signed PDF",
        data=pdf_output,
        file_name=f"SalarySlip_{name}_{month}.pdf",
        mime="application/pdf"
    )
    st.success("Professional Slip with Watermark & Sign is Ready!")
