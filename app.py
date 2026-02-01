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
        self.cell(45, h, "Employee Name", 1); self.set_font('Arial', '', 10); self.cell(5
