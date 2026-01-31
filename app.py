import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from streamlit_folium import st_folium
import folium

# --- DATABASE ---
conn = sqlite3.connect('rmc_pro_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, grade TEXT, qty REAL, rate REAL, total REAL, date TEXT, site_lat REAL, site_lon REAL)')
c.execute('CREATE TABLE IF NOT EXISTS inventory (item TEXT PRIMARY KEY, stock REAL)')
conn.commit()

# --- HELPER: PDF GENERATOR ---
def create_pdf(cust, grade, qty, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="RMC DELIVERY TICKET & CERTIFICATE", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Customer: {cust}", ln=True)
    pdf.cell(200, 10, txt=f"Concrete Grade: {grade}", ln=True)
    pdf.cell(200, 10, txt=f"Quantity: {qty} m3", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount: Rs. {total}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 20, txt="Certified: Quality Tested & Approved", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.set_page_config(page_title="RMC Enterprise Pro", layout="wide")
menu = ["Dashboard", "Sales & GPS Map", "Inventory", "Reports & Certificates"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Dashboard":
    st.title("🏗️ RMC Business Command Center")
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", "₹ 5,40,000")
    col2.metric("Stock Level", "Cement: 85 Tons")

elif choice == "Sales & GPS Map":
    st.subheader("New Dispatch with Site Location")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        with st.form("sales"):
            cust = st.text_input("Customer Name")
            grade = st.selectbox("Grade", ["M20", "M25", "M30", "M40"])
            qty = st.number_input("Qty (m3)")
            rate = st.number_input("Rate")
            st.write("Select Site on Map Right side ➡️")
            lat = st.session_get("lat", 28.6139) # Default Delhi
            lon = st.session_get("lon", 77.2090)
            
            if st.form_submit_button("Save & Generate Certificate"):
                total = qty * rate
                c.execute('INSERT INTO orders (customer, grade, qty, rate, total, date, site_lat, site_lon) VALUES (?,?,?,?,?,?,?,?)',
                          (cust, grade, qty, rate, total, str(datetime.now().date()), lat, lon))
                conn.commit()
                st.success("Order Saved!")
                pdf_data = create_pdf(cust, grade, qty, total)
                st.download_button("Download Certificate/Bill", data=pdf_data, file_name="RMC_Ticket.pdf")

    with col_b:
        st.write("Click on Map to set Delivery Site")
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)
        m.add_child(folium.LatLngPopup())
        map_data = st_folium(m, height=400, width=500)
        if map_data and map_data['last_clicked']:
            st.session_state["lat"] = map_data['last_clicked']['lat']
            st.session_state["lon"] = map_data['last_clicked']['lng']
            st.write(f"Location Set: {st.session_state['lat']}, {st.session_state['lon']}")

elif choice == "Reports & Certificates":
    st.subheader("Order History & Map View")
    df = pd.DataFrame(c.execute('SELECT * FROM orders').fetchall(), columns=['ID','Cust','Grade','Qty','Rate','Total','Date','Lat','Lon'])
    st.dataframe(df)
    
    # Map with all delivery points
    st.subheader("All Delivery Sites")
    m_all = folium.Map(location=[28.6139, 77.2090], zoom_start=10)
    for idx, row in df.iterrows():
        folium.Marker([row['Lat'], row['Lon']], popup=f"{row['Cust']} - {row['Grade']}").add_to(m_all)
    st_folium(m_all, height=500, width=1000)
