import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd

# --- PDF GENERATOR CLASS ---
class SalarySlip(FPDF):
    def header(self):
        # Company Name
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'GLOBAL RMC & CONSTRUCTIONS PVT LTD', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Plot No. 45, Industrial Area, Phase-1, New Delhi', 0, 1, 'C')
        self.ln(10)

    def create_slip(self, data):
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Salary Slip for {data['month']}", 1, 1, 'C')
        
        # Employee Info Table
        self.set_font('Arial', '', 10)
        self.ln(5)
        col_width = 45
        row_height = 8
        
        details = [
            ["Emp Name:", data['name'], "Emp ID:", data['emp_id']],
            ["Department:", data['dept'], "Designation:", data['desig']],
            ["Bank A/c:", data['bank_acc'], "Payment Mode:", data['pay_mode']]
        ]
        
        for row in details:
            self.set_font('Arial', 'B', 10)
            self.cell(col_width, row_height, row[0], border=1)
            self.set_font('Arial', '', 10)
            self.cell(col_width, row_height, row[1], border=1)
            self.set_font('Arial', 'B', 10)
            self.cell(col_width, row_height, row[2], border=1)
            self.set_font('Arial', '', 10)
            self.cell(col_width, row_height, row[3], border=1, ln=1)

        self.ln(10)
        
        # Earnings and Deductions Header
        self.set_font('Arial', 'B', 10)
        self.cell(95, row_height, "EARNINGS", border=1, align='C')
        self.cell(95, row_height, "DEDUCTIONS", border=1, align='C', ln=1)
        
        # Salary Rows
        self.set_font('Arial', '', 10)
