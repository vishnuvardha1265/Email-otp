# libraries
import streamlit as st
import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# loading environment variables
EMAIL = st.secrets["EMAIL_USER"]
PASSWORD = st.secrets["EMAIL_PASS"]

# start building frontend
st.title(" Email OTP Verification")

# intialize the session state
if "otp" not in st.session_state:
    st.session_state.otp = None

with st.form("otp_form"):
    user_email = st.text_input("Enter the email address:")
    send_clicked = st.form_submit_button("Send OTP")

    if send_clicked:
        if EMAIL is None or PASSWORD is None:
            st.error("Email or Password missing in .env file")
        elif user_email == "":
            st.warning("Please enter valid email id")
        else:
            st.session_state.otp = random.randint(1111,9999)
            body = f"OTP send: {st.session_state.otp}"

            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = user_email
            msg["Subject"] = "OTP for Verification"
            msg.attach(MIMEText(body, "plain"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.send_message(msg)
                server.quit()

                st.success(f"OTP sent successfully on {user_email}")
            except:
                st.error("Athentication Failed: plz check your emailID & password")

if st.session_state.otp:
    entered_otp = st.text_input("Enter the received OTP")
    if st.button("Verify OTP"):
        try:
            if int(entered_otp) == st.session_state.otp:
                st.success("Hurray OTP matched successfully")
                st.session_state.otp = None
            else:
                st.error("Invaild OTP, Please try again")
        except ValueError:
            st.warning("Enter only 4 digit OTP")
