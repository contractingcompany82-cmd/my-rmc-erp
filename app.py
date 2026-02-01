import streamlit as st
from fpdf import FPDF

# --- PROFESSIONAL PDF CLASS WITH WATERMARK ---
class ProfessionalSalarySlip(FPDF):
    def header(self):
        # Header Details
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, st.session_state.comp_name.upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Industrial Area, Phase-II, New Delhi', 0, 1, 'C')
        self.cell(0, 5, f"GSTIN: {st.session_state.comp_gst}", 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32)

    def add_watermark(self):
        # Faint Gray Watermark in Background
        self.set_font('Arial', 'B', 50)
        self.set_text_color(240, 240, 240) # Bahut halka gray
        self.rotate(45, 100, 150)
        self.text(40, 190, st.session_state.comp_name.upper())
        self.rotate(0) # Reset Rotation
        self.set_text_color(0, 0, 0) # Reset Color to Black

    def generate_slip(self, d):
        self.add_page()
        self.add_watermark()
        self.ln(10)
        
        # Payslip Header
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, f"PAYSLIP FOR {d['month'].upper()}", 1, 1, 'C', True)
        
        # Employee Table
        self.set_font('Arial', 'B', 10)
        h = 8
        self.cell(45, h, "Employee Name", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['name'], 1)
        self.set_font('Arial', 'B', 10); self.cell(45, h, "Employee ID", 1); self.set_font('Arial', '', 10); self.cell(50, h, d['id'], 1, 1)
        
        # Earnings/Deductions Tables
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(95, h, "EARNINGS", 1, 0, 'C', True)
        self.cell(95, h, "DEDUCTIONS", 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        items = [
            ("Basic Salary", d['basic'], "PF Deduction", d['pf']),
            ("Allowances", d['allowance'], "ESIC", d['esic']),
            ("Special Pay", d['special'], "TDS / Tax", d['tds'])
        ]
        
        for item in items:
            self.cell(60, h, item[0], 1); self.cell(35, h, f"{item[1]:.2f}", 1, 0, 'R')
            self.cell(60, h, item[2], 1); self.cell(35, h, f"{item[3]:.2f}", 1, 1, 'R')

        # Net Salary
        gross = d['basic'] + d['allowance'] + d['special']
        total_ded = d['pf'] + d['esic'] + d['tds']
        net = gross - total_ded
        
        self.set_font('Arial', 'B', 11)
        self.cell(190, 12, f"NET PAYABLE: Rs. {net:,.2f}", 1, 1, 'C', True)

        # DIGITAL SIGNATURE SECTION
        self.ln(30)
        # Box for Digital Sign
        self.set_draw_color(0, 102, 204) # Blue border for sign
        self.set_line_width(0.5)
        self.rect(130, 230, 60, 30) 
        
        self.set_xy(130, 235)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.cell(60, 5, "DIGITALLY SIGNED BY", 0, 1, 'C')
        self.set_font('Arial', 'B', 10)
        self.cell(60, 5, st.session_state.comp_name.upper(), 0, 1, 'C')
        self.set_font('Arial', '', 7)
        self.cell(60, 5, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 0, 1, 'C')
        self.cell(60, 5, "Verified ERP Document", 0, 1, 'C')

# --- STREAMLIT UI ---
import st_from_datetime_import_datetime # (Ensure datetime is imported)
from datetime import datetime

st.title("🛡️ Professional ERP: Salary Slip")

# Sidebar for settings
with st.sidebar:
    st.session_state.comp_name = st.text_input("Company Name", "Global RMC Pvt Ltd")
    st.session_state.comp_gst = st.text_input("GSTIN", "07AAAAA0000A1Z5")

# Form Inputs
with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Employee Name")
        emp_id = st.text_input("Emp ID")
        month = st.selectbox("Month", ["Jan 2026", "Feb 2026"])
    with c2:
        basic = st.number_input("Basic", value=25000)
        pf = st.number_input("PF", value=1800)
        allowance = st.number_input("Allowance", value=5000)
        tds = st.number_input("TDS", value=0)
    
    submit = st.form_submit_button("Generate Slip")

if submit:
    data = {
        'name': name, 'id': emp_id, 'month': month,
        'basic': basic, 'pf': pf, 'allowance': allowance,
        'tds': tds, 'esic': 500, 'special': 2000
    }
    pdf = ProfessionalSalarySlip()
    pdf.generate_slip(data)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    st.download_button("📥 Download Digitally Signed PDF", pdf_bytes, f"Slip_{name}.pdf", "application/pdf")
    st.success("Bhai, Slip ready hai watermark aur digital sign ke sath!")
