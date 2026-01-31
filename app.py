import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect('rmc_complete_erp.db', check_same_thread=False)
c = conn.cursor()

# Tables setup
c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, grade TEXT, qty REAL, rate REAL, total REAL, date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, category TEXT, amount REAL, remarks TEXT, date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (item TEXT PRIMARY KEY, stock REAL)''')
conn.commit()

# Inventory initialize (Sirf pehli baar ke liye)
items = [('Cement', 100.0), ('Sand', 500.0), ('Agg_10mm', 300.0), ('Agg_20mm', 400.0)]
for item, stock in items:
    c.execute('INSERT OR IGNORE INTO inventory VALUES (?,?)', (item, stock))
conn.commit()

# --- APP UI ---
st.set_page_config(page_title="RMC Full Enterprise ERP", layout="wide")
st.sidebar.title("🏗️ RMC FULL ERP")
menu = ["📈 Dashboard", "📝 Sales & Billing", "💰 Finance/Accounts", "📦 Inventory", "📑 Reports"]
choice = st.sidebar.selectbox("Modules", menu)

# --- MODULE 1: DASHBOARD ---
if choice == "📈 Dashboard":
    st.subheader("Business Overview")
    sales_data = c.execute('SELECT SUM(total) FROM orders').fetchone()[0] or 0
    exp_data = c.execute('SELECT SUM(amount) FROM expenses').fetchone()[0] or 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{sales_data:,.2f}")
    col2.metric("Total Expenses", f"₹{exp_data:,.2f}")
    col3.metric("Net Profit", f"₹{(sales_data - exp_data):,.2f}")

# --- MODULE 2: SALES & BILLING ---
elif choice == "📝 Sales & Billing":
    st.subheader("New Dispatch & Invoice")
    with st.form("sales_form"):
        cust = st.text_input("Customer Name")
        grade = st.selectbox("Grade", ["M20", "M25", "M30", "M40"])
        qty = st.number_input("Quantity (m³)", min_value=1.0)
        rate = st.number_input("Rate per m³ (₹)", min_value=1.0)
        date = st.date_input("Date")
        submit = st.form_submit_button("Generate Bill")
        
        if submit:
            total = qty * rate
            c.execute('INSERT INTO orders (customer, grade, qty, rate, total, date) VALUES (?,?,?,?,?,?)',
                      (cust, grade, qty, rate, total, str(date)))
            # Auto-deduct inventory (Simple logic: 1m3 uses ~0.35T cement)
            c.execute('UPDATE inventory SET stock = stock - ? WHERE item = "Cement"', (qty * 0.35,))
            conn.commit()
            st.success(f"Bill Generated! Total Amount: ₹{total}")

# --- MODULE 3: FINANCE/ACCOUNTS ---
elif choice == "💰 Finance/Accounts":
    st.subheader("Expense Management")
    with st.expander("Add New Expense (Diesel, Salary, Maintenance)"):
        cat = st.selectbox("Category", ["Diesel", "Labor Salary", "Maintenance", "Electricity", "Other"])
        amt = st.number_input("Amount (₹)", min_value=1.0)
        rem = st.text_area("Remarks")
        if st.button("Save Expense"):
            c.execute('INSERT INTO expenses (category, amount, remarks, date) VALUES (?,?,?,?)',
                      (cat, amt, rem, str(datetime.now().date())))
            conn.commit()
            st.success("Expense Recorded")

# --- MODULE 4: INVENTORY ---
elif choice == "📦 Inventory":
    st.subheader("Live Stock Status")
    data = c.execute('SELECT * FROM inventory').fetchall()
    st.table(pd.DataFrame(data, columns=['Material Name', 'Current Stock (Tons)']))
    
    with st.expander("Refill Stock (Purchase)"):
        item_to_add = st.selectbox("Select Material", ["Cement", "Sand", "Agg_10mm", "Agg_20mm"])
        add_qty = st.number_input("Added Quantity", min_value=1.0)
        if st.button("Update Stock"):
            c.execute('UPDATE inventory SET stock = stock + ? WHERE item = ?', (add_qty, item_to_add))
            conn.commit()
            st.experimental_rerun()

# --- MODULE 5: REPORTS ---
elif choice == "📑 Reports":
    st.subheader("Download Business Reports")
    tab1, tab2 = st.tabs(["Sales Report", "Expense Report"])
    with tab1:
        df_s = pd.DataFrame(c.execute('SELECT * FROM orders').fetchall(), columns=['ID','Customer','Grade','Qty','Rate','Total','Date'])
        st.dataframe(df_s)
    with tab2:
        df_e = pd.DataFrame(c.execute('SELECT * FROM expenses').fetchall(), columns=['ID','Category','Amount','Remarks','Date'])
        st.dataframe(df_e)
