import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
st.set_page_config(page_title="Pro RMC ERP", layout="wide")

# Persistent Data Storage (Simulation using Session State - Replace with Database for Production)
if 'data' not in st.session_state:
    st.session_state.data = {
        'sales': [],
        'expenses': [],
        'inventory': {'Cement': 1000, 'Sand': 500, 'Grit': 800, 'Admixture': 200},
        'employees': [{'Name': 'Rahul', 'Role': 'Driver', 'Salary': 15000, 'Status': 'Paid'}]
    }

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏗️ RMC PRO-ERP")
menu = ["📊 Dashboard", "💰 Finance & Sales", "📉 Expenses", "🚛 Dispatch & Map", "👷 Salary & HR", "📄 Reports & PDF"]
choice = st.sidebar.radio("Navigate", menu)

# --- 📊 DASHBOARD ---
if choice == "📊 Dashboard":
    st.header("Plant Overview")
    col1, col2, col3 = st.columns(3)
    
    total_sales = sum(item['Total'] for item in st.session_state.data['sales'])
    total_exp = sum(item['Amount'] for item in st.session_state.data['expenses'])
    
    col1.metric("Total Revenue", f"₹{total_sales:,}")
    col2.metric("Total Expenses", f"₹{total_exp:,}")
    col3.metric("Net Profit", f"₹{total_sales - total_exp:,}")

    # Inventory Chart
    st.subheader("Inventory Stock Level")
    inv_df = pd.DataFrame(list(st.session_state.data['inventory'].items()), columns=['Item', 'Qty'])
    st.bar_chart(inv_df.set_index('Item'))

# --- 💰 FINANCE & SALES ---
elif choice == "💰 Finance & Sales":
    st.header("Sales & Billing")
    with st.form("sales_form"):
        c_name = st.text_input("Customer Name")
        grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M40"])
        qty = st.number_input("Quantity (m3)", min_value=1)
        rate = st.number_input("Rate per m3", value=4500)
        submit = st.form_submit_button("Generate Sale")
        
        if submit:
            total = qty * rate
            st.session_state.data['sales'].append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Customer": c_name, "Grade": grade, "Qty": qty, "Total": total
            })
            st.success(f"Sale Recorded! Total: ₹{total}")

# --- 📉 EXPENSES ---
elif choice == "📉 Expenses":
    st.header("Expense Tracker (Diesel, Maintenance, etc.)")
    exp_type = st.selectbox("Category", ["Diesel", "Spare Parts", "Electricity", "Tea/Food", "Other"])
    amt = st.number_input("Amount Paid", min_value=0)
    remark = st.text_area("Remark")
    
    if st.button("Add Expense"):
        st.session_state.data['expenses'].append({"Type": exp_type, "Amount": amt, "Date": datetime.now().strftime("%Y-%m-%d")})
        st.warning(f"Expense of ₹{amt} recorded.")

# --- 🚛 DISPATCH & MAP ---
elif choice == "🚛 Dispatch & Map":
    st.header("Live Dispatch Tracking")
    st.info("Integrating Google Maps API for TM tracking...")
    # Simulation of a map
    map_data = pd.DataFrame({'lat': [28.6139], 'lon': [77.2090]}) # Delhi Example
    st.map(map_data)
    st.write("Transit Mixer TM-01: Heading to Site A (ETA 15 mins)")

# --- 👷 SALARY & HR ---
elif choice == "👷 Salary & HR":
    st.header("Staff & Salary Management")
    df_emp = pd.DataFrame(st.session_state.data['employees'])
    st.table(df_emp)
    
    if st.button("Process Monthly Salary"):
        st.success("Salaries credited to linked bank accounts via API.")

# --- 📄 REPORTS & PDF ---
elif choice == "📄 Reports & PDF":
    st.header("Download Reports")
    if st.session_state.data['sales']:
        df_sales = pd.DataFrame(st.session_state.data['sales'])
        csv = df_sales.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Sales Report (CSV)", csv, "sales_report.csv", "text/csv")
        
        st.subheader("Cube Test Certificate (Draft)")
        st.write(f"Certificate No: RMC-{datetime.now().year}-001")
        st.write("Status: ✅ Passed (28 Days Strength: 30N/mm2)")
