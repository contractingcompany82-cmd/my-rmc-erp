import streamlit as st
from modules import sales  # You can import purchase, finance, hr, etc later

st.set_page_config(page_title="Readymix ERP", layout="wide")
st.title("Readymix ERP Dashboard")

menu = ["Sales"]  # Add Purchase, Finance, HR, Expense later
choice = st.sidebar.selectbox("Select Module", menu)

if choice == "Sales":
    sales.run()
