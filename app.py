import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Custom Expense ERP", layout="wide")

# --- DATABASE (Storage) ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'categories' not in st.session_state:
    st.session_state.categories = ["Diesel", "Raw Material", "Staff Salary", "Repairing", "Office Exp"]

# --- SIDEBAR: CUSTOMIZATION AREA ---
st.sidebar.header("⚙️ ERP Customization")

# Add New Category
new_cat = st.sidebar.text_input("Nayi Category Add Karein")
if st.sidebar.button("Add Category"):
    if new_cat and new_cat not in st.session_state.categories:
        st.session_state.categories.append(new_cat)
        st.sidebar.success(f"{new_cat} Add ho gayi!")

# Remove Category
rem_cat = st.sidebar.selectbox("Category Delete Karein", st.session_state.categories)
if st.sidebar.button("Delete Category"):
    st.session_state.categories.remove(rem_cat)
    st.sidebar.warning(f"{rem_cat} Hata di gayi!")

# --- MAIN SCREEN ---
st.title("💰 Expense Management System (RMC Custom)")
st.markdown("---")

# Layout: Form and Summary
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Naya Kharcha Dalein")
    with st.form("exp_form", clear_on_submit=True):
        date = st.date_input("Tareekh", datetime.now())
        cat = st.selectbox("Kharch ki Category", st.session_state.categories)
        amount = st.number_input("Amount (Rs.)", min_value=0, step=100)
        pay_mode = st.radio("Payment Mode", ["Cash", "Online/Bank", "Cheque"])
        remark = st.text_input("Remark (Kisko diya / Kis liye)")
        
        submit = st.form_submit_button("Record Expense")
        
        if submit:
            entry = {
                "Date": date,
                "Category": cat,
                "Amount": amount,
                "Mode": pay_mode,
                "Remark": remark
            }
            st.session_state.expenses.append(entry)
            st.success("Kharcha Save Ho Gaya!")

with col2:
    st.subheader("📊 Kharchon ka Hisab")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        
        # Summary Metrics
        total_exp = df['Amount'].sum()
        st.metric("Total Kharcha", f"₹{total_exp:,}")
        
        # Data Table
        st.dataframe(df, use_container_width=True)
        
        # Category wise Chart
        st.subheader("Category Wise Analysis")
        cat_total = df.groupby('Category')['Amount'].sum()
        st.bar_chart(cat_total)
        
        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Excel/CSV Download Karein", csv, "expenses.csv", "text/csv")
    else:
        st.info("Abhi koi kharcha record nahi kiya gaya hai.")

# --- CLEAR ALL DATA ---
if st.sidebar.button("⚠️ Clear All Data"):
    st.session_state.expenses = []
    st.rerun()
