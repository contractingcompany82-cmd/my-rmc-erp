import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="RMC Enterprise Resource Planning", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE INITIALIZATION ---
# Real-world mein yahan SQL connect hoga, abhi ke liye Session State hai.
if 'db_sales' not in st.session_state: st.session_state.db_sales = []
if 'db_expenses' not in st.session_state: st.session_state.db_expenses = []
if 'db_inventory' not in st.session_state: 
    st.session_state.db_inventory = {"Cement": 5000, "Sand": 2000, "Aggregates": 3500, "Admixture": 500}
if 'db_staff' not in st.session_state: 
    st.session_state.db_staff = [{"ID": "001", "Name": "Admin", "Role": "Manager", "Salary": 50000}]

# --- 3. MODULAR FUNCTIONS (Yahan se Add/Remove karein) ---

def show_dashboard():
    st.header("📊 Business Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = sum(x['Total'] for x in st.session_state.db_sales)
    total_expense = sum(x['Amount'] for x in st.session_state.db_expenses)
    
    col1.metric("Total Sales", f"₹{total_revenue:,}")
    col2.metric("Total Expenses", f"₹{total_expense:,}")
    col3.metric("Profit/Loss", f"₹{total_revenue - total_expense:,}")
    col4.metric("Active Sites", len(set([x['Client'] for x in st.session_state.db_sales])))
    
    st.subheader("Inventory Stock")
    st.bar_chart(pd.DataFrame.from_dict(st.session_state.db_inventory, orient='index', columns=['Qty']))

def manage_sales():
    st.header("💰 Sales & Dispatch")
    with st.expander("➕ New Dispatch Entry"):
        with st.form("sales_form"):
            c_
