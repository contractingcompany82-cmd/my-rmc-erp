import streamlit as st
import sqlite3
import pandas as pd

# Database Connection Setup
conn = sqlite3.connect('rmc_erp.db', check_same_thread=False)
c = conn.cursor()

# Tables Banana (Order aur Inventory ke liye)
c.execute('CREATE TABLE IF NOT EXISTS orders(customer TEXT, grade TEXT, qty REAL, site TEXT, date TEXT)')
conn.commit()

st.set_page_config(page_title="RMC Pro-ERP", layout="wide")

st.title("🏗️ RMC Production & Order ERP")

menu = ["Dashboard", "Order Entry", "View Records", "Inventory Management"]
choice = st.sidebar.selectbox("Control Panel", menu)

if choice == "Dashboard":
    st.subheader("Live Plant Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Month Production", "1,250 m³")
    col2.metric("Pending Orders", "5")
    col3.metric("Fleet Status", "8 Active / 2 Maintenance")

elif choice == "Order Entry":
    st.subheader("📝 New Booking")
    with st.form("entry_form"):
        cust = st.text_input("Customer Name")
        grade = st.selectbox("Grade", ["M15", "M20", "M25", "M30", "M40", "M50"])
        qty = st.number_input("Quantity (m³)", min_value=0.5)
        site = st.text_input("Site Address")
        date = st.date_input("Delivery Date")
        submit = st.form_submit_button("Save Order")
        
        if submit:
            c.execute('INSERT INTO orders (customer, grade, qty, site, date) VALUES (?,?,?,?,?)', 
                      (cust, grade, qty, site, str(date)))
            conn.commit()
            st.success(f"Order for {cust} saved successfully!")

elif choice == "View Records":
    st.subheader("📊 All Orders")
    data = c.execute('SELECT * FROM orders').fetchall()
    df = pd.DataFrame(data, columns=['Customer', 'Grade', 'Qty', 'Site', 'Date'])
    st.dataframe(df, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Excel/CSV Download karein", data=csv, file_name="RMC_Report.csv")

elif choice == "Inventory Management":
    st.subheader("📉 Raw Material Stock")
    st.info("Batching Plant se API connect karke ye data auto-update ho sakta hai.")
    st.write("Current Stock: Cement (45T), Flyash (20T), Admixture (500L)")