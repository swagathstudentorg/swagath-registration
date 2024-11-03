import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a connection object
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Define form fields
st.title("Event Registration")

email = st.text_input("Email")
full_name = st.text_input("Full Name")
mobile_no = st.text_input("Mobile Number")
is_student = st.radio("Are you a Student?", ("Yes", "No"))
home_country = st.text_input("Home Country")
need_ride = st.radio("Do you need a ride?", ("Yes", "No"))
pickup_details = st.text_input("Pickup point (if needed)") if need_ride == "Yes" else ""
special_needs = st.text_area("Special needs / prayer requests")
comments = st.text_area("Comments")

# Form submission
if st.button("Submit"):
    # Structure data
    data = {
        "Email": email,
        "Full Name": full_name,
        "Mobile Number": mobile_no,
        "Are you a Student?": is_student,
        "Home Country": home_country,
        "Do you need a ride?": need_ride,
        "Pickup point": pickup_details,
        "Special needs / prayer requests": special_needs,
        "Comments": comments,
    }
    df = pd.DataFrame([data])
    conn.append(data=df)
    st.success("Thank you for registering!")
