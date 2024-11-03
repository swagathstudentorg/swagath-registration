import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Sidebar content
st.sidebar.image("swagath_wallpaper3.webp", use_column_width=True)
st.sidebar.title("Swagath Registrations")

# Fetch and display registration data in the sidebar
try:
    registration_data = conn.read(worksheet="Responses")
    if registration_data.empty:
        st.sidebar.warning("No registrations found.")
    else:
        st.sidebar.subheader("All Registrations")
        st.sidebar.dataframe(registration_data)
except Exception as e:
    st.sidebar.error(f"An error occurred: {e}")

# Main content
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
    # Structure new data
    new_data = {
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
    new_df = pd.DataFrame([new_data])

    # Read existing data
    try:
        existing_df = conn.read(worksheet="Responses")
        # Append new data to existing data
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    except Exception as e:
        # If reading fails (e.g., sheet is empty), use new data as the updated data
        updated_df = new_df

    # Update the Google Sheet with the combined data
    conn.update(worksheet="Responses", data=updated_df)

    st.success("Thank you for registering!")
