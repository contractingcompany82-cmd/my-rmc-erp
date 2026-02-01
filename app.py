import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Pro School ERP", layout="wide")

# --- DATABASE INITIALIZATION ---
if 'students' not in st.session_state: st.session_state.students = []
if 'staff' not in st.session_state: st.session_state.staff = []
if 'fees' not in st.session_state: st.session_state.fees = []
if 'classes' not in st.session_state: st.session_state.classes = ["1st", "2nd", "3rd", "10th", "12th"]

# --- SIDEBAR CUSTOMIZATION ---
st.sidebar.title("🏫 School Admin Panel")
menu = st.sidebar.radio("Select Module", ["📊 Dashboard", "🎓 Students", "👩‍🏫 Staff", "💰 Fees/Finance", "⚙️ Setup Classes"])

# --- MODULE 1: SETUP CLASSES (CUSTOMIZATION) ---
if menu == "⚙️ Setup Classes":
    st.header("Customize School Structure")
    new_class = st.text_input("Add New Class (e.g. 11th Science)")
    if st.button("Add Class"):
        if new_class not in st.session_state.classes:
            st.session_state.classes.append(new_class)
            st.success("Class Added!")

# --- MODULE 2: DASHBOARD ---
elif menu == "📊 Dashboard":
    st.header("School Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", len(st.session_state.students))
    c2.metric("Total Staff", len(st.session_state.staff))
    total_fees = sum(f['Amount'] for f in st.session_state.fees)
    c3.metric("Total Fees Collected", f"₹{total_fees:,}")

    

# --- MODULE 3: STUDENTS ---
elif menu == "🎓 Students":
    st.header("Student Admission & Records")
    with st.expander("➕ New Admission"):
        with st.form("stud_form"):
            name = st.text_input("Student Name")
            cls = st.selectbox("Assign Class", st.session_state.classes)
            roll = st.text_input("Roll No.")
            father = st.text_input("Father's Name")
            if st.form_submit_button("Enroll Student"):
                st.session_state.students.append({"Roll": roll, "Name": name, "Class": cls, "Father": father})
                st.success("Admission Successful!")
    
    if st.session_state.students:
        st.subheader("Student Directory")
        st.dataframe(pd.DataFrame(st.session_state.students), use_container_width=True)

# --- MODULE 4: STAFF ---
elif menu == "👩‍🏫 Staff":
    st.header("Teacher & Staff Management")
    with st.form("staff_form"):
        s_name = st.text_input("Staff Name")
        s_role = st.selectbox("Role", ["Teacher", "Principal", "Admin", "Driver", "Peon"])
        if st.form_submit_button("Add Staff"):
            st.session_state.staff.append({"Name": s_name, "Role": s_role})
            st.success("Staff Record Added!")
    
    st.table(pd.DataFrame(st.session_state.staff))

# --- MODULE 5: FEES/FINANCE ---
elif menu == "💰 Fees/Finance":
    st.header("Fee Collection System")
    if st.session_state.students:
        stud_list = [f"{s['Name']} (Roll: {s['Roll']})" for s in st.session_state.students]
        selected_stud = st.selectbox("Select Student", stud_list)
        amount = st.number_input("Fee Amount Paid", min_value=0)
        
        if st.button("Submit Fee"):
            st.session_state.fees.append({
                "Date": datetime.now().date(),
                "Student": selected_stud,
                "Amount": amount
            })
            st.success(f"Fee of ₹{amount} recorded for {selected_stud}")
        
        if st.session_state.fees:
            st.subheader("Recent Transactions")
            st.dataframe(pd.DataFrame(st.session_state.fees))
    else:
        st.warning("Please add students first to collect fees!")
