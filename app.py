import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="RMC ERP - India", layout="wide")

# App Title
st.title("🏗️ RMC Plant Management System")

# Sidebar for Navigation
menu = ["Dashboard", "Inventory Management", "Dispatch Entry", "Billing/Invoices"]
choice = st.sidebar.selectbox("Menu", menu)

# --- INVENTORY DATA (Dummy Storage) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        'Cement (Bags)': 500,
        'Sand (Tons)': 150,
        'Aggregates (Tons)': 300,
        'Admixture (Liters)': 1000
    }

# --- DISPATCH DATA ---
if 'dispatches' not in st.session_state:
    st.session_state.dispatches = []

# --- 1. DASHBOARD ---
if choice == "Dashboard":
    st.subheader("Current Stock Status")
    cols = st.columns(4)
    for i, (item, qty) in enumerate(st.session_state.inventory.items()):
        cols[i].metric(label=item, value=qty)
    
    st.subheader("Recent Dispatches")
    if st.session_state.dispatches:
        df = pd.DataFrame(st.session_state.dispatches)
        st.table(df)
    else:
        st.info("No dispatches yet today.")

# --- 2. INVENTORY MANAGEMENT ---
elif choice == "Inventory Management":
    st.subheader("Update Stock")
    item_to_update = st.selectbox("Select Material", list(st.session_state.inventory.keys()))
    new_qty = st.number_input("Add Quantity", min_value=0)
    
    if st.button("Update Inventory"):
        st.session_state.inventory[item_to_update] += new_qty
        st.success(f"Updated {item_to_update} successfully!")

# --- 3. DISPATCH ENTRY ---
elif choice == "Dispatch Entry":
    st.subheader("New Concrete Dispatch (TM Entry)")
    with st.form("dispatch_form"):
        client = st.text_input("Client Name")
        grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        qty_m3 = st.number_input("Quantity (Cubic Meter)", min_value=1.0)
        tm_number = st.text_input("Transit Mixer (TM) No.")
        
        submitted = st.form_submit_button("Generate Dispatch Note")
        
        if submitted:
            # Simple Logic: 1m3 concrete uses approx 6 bags cement
            cement_needed = qty_m3 * 6 
            if st.session_state.inventory['Cement (Bags)'] >= cement_needed:
                st.session_state.inventory['Cement (Bags)'] -= cement_needed
                new_entry = {
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Client": client,
                    "Grade": grade,
                    "Qty": qty_m3,
