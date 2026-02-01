import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- PROFESSIONAL PDF CLASS WITH WATERMARK & SIGN ---
class ProfessionalSalarySlip(FPDF):
    def header(self):
        # Company Header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, st.session_state.get('comp_name', 'COMPANY NAME').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Industrial Area, Phase-II, New Delhi', 0, 1, 'C')
        self.cell(0, 5, f"GSTIN: {st.session_state.get('comp_gst', 'N/A')}", 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32)

    def add_watermark(self):
        # Faint Gray Watermark
        self.set_font('Arial', 'B', 40)
        self.set_text_color(240, 240, 240) 
        # Savdhan: Watermark placement
        self.set_xy(50, 150)
        self.cell(0, 0, st.session_state.get('comp_name', 'CONFIDENTIAL').upper(), 0, 0, 'C')
        self.set_text_color(0, 0, 0) # Reset color

    def generate_slip(self, d):
        self.add_page()
        self.add_watermark()
        self.ln(10)
        
        # Payslip Title
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, f"PAYSLIP FOR {d['month'].upper()}", 1, 1, 'C', True)
        
        # Employee Table
        self.set_font('Arial', 'B', 10)
        h = 8
        self.cell(45, h, "Employee Name", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['name'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Employee ID", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['id'], 1, 1)
        
        # Earnings/Deductions
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(95, h, "EARNINGS", 1, 0, 'C', True)
        self.cell(95, h, "DEDUCTIONS", 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        # Row 1
        self.cell(60, h, "Basic Salary", 1); self.cell(35, h, f"{d['basic']:.2f}", 1, 0, 'R')
        self.cell(60, h, "PF Deduction", 1); self.cell(35, h, f"{d['pf']:.2f}", 1, 1, 'R')
        # Row 2
        self.cell(60, h, "Allowances", 1); self.cell(35, h, f"{d['allowance']:.2f}", 1, 0, 'R')
        self.cell(60, h, "TDS / Tax", 1); self.cell(35, h, f"{d['tds']:.2f}", 1, 1, 'R')

        # Net Salary
        gross = d['basic'] + d['allowance']
        total_ded = d['pf'] + d['tds']
        net = gross - total_ded
        
        self.set_font('Arial', 'B', 11)
        self.cell(190, 12, f"NET PAYABLE: Rs. {net:,.2f}", 1, 1, 'C', True)

        # DIGITAL SIGNATURE BOX
        self.ln(30)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.rect(130, 230, 60, 30) 
        
        self.set_xy(130, 235)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.cell(60, 5, "DIGITALLY SIGNED BY", 0, 1, 'C')
        self.set_font('Arial', 'B', 9)
        self.cell(60, 5, st.session_state.get('comp_name', 'COMPANY').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 7)
        self.cell(60, 5, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 0, 1, 'C')
        self.cell(60, 5, "Verified Document", 0, 1, 'C')

# --- STREAMLIT UI ---
st.title("🛡️ Professional Salary ERP")

with st.sidebar:
    st.header("Settings")
    st.session_state.comp_name = st.text_input("Company Name", "Global RMC Pvt Ltd")
    st.session_state.comp_gst = st.text_input("GSTIN", "07AAAAA0000A1Z5")

with st.form("salary_form"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Employee Name", "Rahul Kumar")
        emp_id = st.text_input("Emp ID", "RMC-001")
        month = st.selectbox("Month", ["January 2026", "February 2026"])
    with c2:
        basic = st.number_input("Basic Salary", value=25000)
        allowance = st.number_input("Allowance", value=5000)
        pf = st.number_input("PF", value=1800)
        tds = st.number_input("TDS", value=0)
    
    submit = st.form_submit_button("Generate PDF Slip")

if submit:
    data = {
        'name': name, 'id': emp_id, 'month': month,
        'basic': basic, 'pf': pf, 'allowance': allowance, 'tds': tds
    }
    pdf = ProfessionalSalarySlip()
    pdf.generate_slip(data)
    
    # S = String output for download
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    st.download_button(
        label="📥 Download Digitally Signed PDF",
        data=pdf_bytes,
        file_name=f"SalarySlip_{name}.pdf",
        mime="application/pdf"
    )
    st.success("Bhai, Slip ready hai!")
