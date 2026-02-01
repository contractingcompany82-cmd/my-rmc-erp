import streamlit as st
import pandas as pd
from datetime import datetime

# Page Settings
st.set_page_config(page_title="RMC ERP Pro", layout="wide")

# Title
st.title("🏗️ RMC Enterprise Resource Planning (ERP)")
st.markdown("---")

# --- DATABASE IN MEMORY ---
if 'sales' not in st.session_state: st.session_state.sales = []
if 'expenses' not in st.session_state: st.session_state.expenses = []
if 'inventory' not in st.session_state: 
    st.session_state.inventory = {"Cement": 1000, "Sand": 500, "Grit": 800}
if 'staff' not in st.session_state:
    st.session_state.staff = [{"Name": "Rahul", "Role": "Driver", "Salary": 15000}]

# --- SIDEBAR MENU ---
menu = st.sidebar.selectbox("Go to Module", 
    ["📊 Dashboard", "💰 Sales & Billing", "📉 Expenses & Finance", "👷 Staff & Salary", "📦 Inventory"])

# --- 📊 DASHBOARD ---
if menu == "📊 Dashboard":
    st.subheader("Business Summary")
    c1, c2, c3 = st.columns(3)
    
    rev = sum(s['Total'] for s in st.session_state.sales)
    exp = sum(e['Amount'] for e in st.session_state.expenses)
    
    c1.metric("Total Revenue", f"₹{rev}")
    c2.metric("Total Expenses", f"₹{exp}")
    c3.metric("Profit", f"₹{rev - exp}")

    st.markdown("---")
    st.subheader("Recent Sales Table")
    if st.session_state.sales:
        st.table(pd.DataFrame(st.session_state.sales))
    else:
        st.write("No sales yet.")

# --- 💰 SALES & BILLING ---
elif menu == "💰 Sales & Billing":
    st.subheader("New Sales Entry")
    with st.form("sale_form"):
        client = st.text_input("Customer Name")
        qty = st.number_input("Quantity (m3)", min_value=1.0)
        rate = st.number_input("Rate per m3", value=4500)
        btn = st.form_submit_button("Generate Bill")
        
        if btn:
            total = qty * rate
            st.session_state.sales.append({"Date": str(datetime.now().date()), "Client": client, "Qty": qty, "Total": total})
            st.success(f"Sale Added! Total: ₹{total}")

# --- 📉 EXPENSES & FINANCE ---
elif menu == "📉 Expenses & Finance":
    st.subheader("Manage Expenses")
    with st.form("exp_form"):
        e_type = st.selectbox("Type", ["Diesel", "Electricity", "Maintenance", "Office"])
        e_amt = st.number_input("Amount", min_value=1)
        if st.form_submit_button("Add Expense"):
            st.session_state.expenses.append({"Type": e_type, "Amount": e_amt, "Date": str(datetime.now().date())})
            st.success("Expense Recorded")
    
    st.table(pd.DataFrame(st.session_state.expenses))

# --- 👷 STAFF & SALARY ---
elif menu == "👷 Staff & Salary":
    st.subheader("Employee Records")
    st.table(pd.DataFrame(st.session_state.staff))
    
    with st.expander("Add New Employee"):
        name = st.text_input("Staff Name")
        role = st.text_input("Role")
        sal = st.number_input("Salary", min_value=0)
        if st.button("Save Staff"):
            st.session_state.staff.append({"Name": name, "Role": role, "Salary": sal})
            st.rerun()

# --- 📦 INVENTORY ---
elif menu == "📦 Inventory":
    st.subheader("Current Stock Status")
    for item, qty in st.session_state.inventory.items():
        st.write(f"**{item}:** {qty}")
    
    new_qty = st.number_input("Add Cement (Bags)", min_value=0)
    if st.button("Update Stock"):
        st.session_state.inventory["Cement"] += new_qty
        st.rerun()
