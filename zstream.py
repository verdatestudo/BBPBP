

# 2025-05-23

import datetime
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import tempfile

from supabase import create_client, Client
from zpbp_stage_one import generate_report

def run_main_app():
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    uploaded_file = st.file_uploader("Upload your spreadsheet", type=["xlsx", "csv"])

    st.header("How To")
    st.markdown("* In BB Preferences, change language to English (UK).")
    st.markdown("* Download your play-by-play to an excel file. See below if you require more detail.")
    st.markdown("* You can upload multiple games at once using the same spreadsheet. Just put each play-by-play data in a different worksheet and give each worksheet a specific name.")
    st.markdown("* Upload here and run this app.")
    st.markdown("* Download the completed spreadsheet.")
    st.markdown("* On google sheets, duplicate a current report and rename it.")
    st.markdown("* Copy and paste the data from this app spreadsheet, into the google sheets spreadsheet.")
    st.markdown("* You should now be able to use the pivot tables and other reports.")

    st.header("Downloading Play-By-Play")
    st.markdown("* Go to the bottom of the PBP.")
    st.markdown("* Select the text while scrolling up all the way to the top.")
    st.markdown("* Once selected, copy and paste into a spreadsheet. It should look like the below image.")
    st.image("zstream_example.png")

    st.header("More")
    st.markdown("* There will be the occasional shot missing. For example if a team shot 40/89 FG, you might see 40/87 or 39/88 or something. This will be because I haven't seen a specific play before and haven't charted it. Let me know and I can add it.")



    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_input:
            temp_input.write(uploaded_file.read())
            input_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_stage1:
            output_path_stage1 = temp_stage1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_stage2:
            output_path_stage2 = temp_stage2.name

        # Step 1: Convert Spreadsheet 1 to Spreadsheet 2
        generate_report(input_path, output_path_stage1, output_path_stage2)

        # Final Download
        with open(output_path_stage2, "rb") as f:
            st.download_button(
                label="Download Final Report",
                data=f,
                file_name="final_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    return None


# def supabase():
#     # Check if user is already logged in
#     if "user" in st.session_state:
#         st.success("Already logged in!")
#         return True
    
#     # Replace with your actual Supabase project URL and anon key
#     SUPABASE_URL = st.secrets["SUPABASE_URL"]
#     SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

#     supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#     st.title("Secure Login")

#     email = st.text_input("Enter your email address", key="email_input")

#     if st.button("Send OTP"):
#         if email:
#             try:
#                 response = supabase.auth.sign_in_with_otp({"email": email})
#                 st.success("An OTP has been sent to your email.")
#             except Exception as e:
#                 st.error(f"Error sending OTP: {e}")


#     otp = st.text_input("Enter the OTP code", key="otp_input")

#     if st.button("Verify OTP"):
#         if email and otp:
#             try:
#                 response = supabase.auth.verify_otp({
#                     "email": email,
#                     "token": otp,
#                     "type": "email"
#                 })

#                 # Check if session exists in response
#                 if not response.session:
#                     st.error("OTP verification failed: no session returned.")
#                     return False

#                 session = response.session  # Get the authenticated session
#                 user_email = session.user.email  # more reliable than response.user
#                 allowed_emails = st.secrets.get("allowed_emails", [])
                
#                 if user_email not in allowed_emails:
#                     st.error("You are not authorized to use this app.")
#                     return False

#                 # Set the session in supabase client so RLS policies recognize the user
#                 if session:
#                     supabase.auth.set_session(session)
#                 else:
#                     st.warning("No session found after OTP verification.")

#                 # Now you can safely insert the login record
#                 supabase.table("logins").insert({
#                     "email": response.user.email,
#                     "login_time": datetime.datetime.utcnow().isoformat()
#                 }).execute()

#                 # # Re-create the Supabase client with the session's token
#                 # authed_supabase = create_client(
#                 #     SUPABASE_URL,
#                 #     SUPABASE_KEY,
#                 #     options={
#                 #         "global": {
#                 #             "headers": {
#                 #                 "Authorization": f"Bearer {session.access_token}"
#                 #             }
#                 #         }
#                 #     }
#                 # )

#                 # # Now you're authenticated for the insert
#                 # authed_supabase.table("logins").insert({
#                 #     "email": user_email,
#                 # }).execute()

#                 # Now you're authenticated for the insert
#                 # supabase.table("logins").insert({
#                 #     "email": user_email,
#                 # }).execute()
                

#                 st.success("You have successfully logged in!")
#                 st.session_state["user"] = response.user

#                 # # Optional: log login
#                 # supabase.table("logins").insert({
#                 #     "email": response.user.email,
#                 # }).execute()

#                 return True

#             except Exception as e:
#                 st.error(f"Error verifying OTP: {e}")

#                 st.success("You have successfully logged in!")
#                 st.session_state["user"] = session.user
#                 return True

#             # response = supabase.auth.verify_otp({
#             #     "email": email,
#             #     "token": otp,
#             #     "type": "email"
#             # })

#             # if response.error:
#             #     st.error(f"Error verifying OTP: {response.error.message}")
#             # else:
#             #     # Check if email is in allowed list
#             #     allowed_emails = st.secrets.get("allowed_emails", [])
#             #     if response.user.email not in allowed_emails:
#             #         st.error("Access denied: You are not authorized to use this app.")
#             #         return False
                
#             #     # Log login
#             #     supabase.table("logins").insert({
#             #         "email": response.user.email,
#             #     }).execute()

#             #     st.success("You have successfully logged in!")
#             #     st.session_state["user"] = response.user
#             #     return True
    
#     return False

def supabase():
    # Check if user is already logged in
    if "user" in st.session_state:
        st.success("Already logged in!")
        return True
    
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    st.title("Secure Login")

    email = st.text_input("Enter your email address", key="email_input")

    if st.button("Send OTP"):
        if email:
            try:
                response = supabase.auth.sign_in_with_otp({"email": email})
                st.success("An OTP has been sent to your email.")
            except Exception as e:
                st.error(f"Error sending OTP: {e}")

    otp = st.text_input("Enter the OTP code", key="otp_input")

    if st.button("Verify OTP"):
        if email and otp:
            try:
                response = supabase.auth.verify_otp({
                    "email": email,
                    "token": otp,
                    "type": "email"
                })

                # Check session presence
                if not response.session:
                    st.error("OTP verification failed: no session returned.")
                    return False

                session = response.session
                user_email = session.user.email

                allowed_emails = st.secrets.get("allowed_emails", [])
                if user_email not in allowed_emails:
                    st.error("You are not authorized to use this app.")
                    return False

                # Set the session so Supabase SDK knows who is logged in
                supabase.auth.set_session(session.access_token, session.refresh_token)

                # Insert login record (RLS should allow this now)
                supabase.table("logins").insert({
                    "email": user_email,
                    "login_time": datetime.datetime.utcnow().isoformat()
                }).execute()

                st.success("You have successfully logged in!")
                st.session_state["user"] = session.user
                return True

            except Exception as e:
                st.error(f"Error verifying OTP: {e}")
                return False
    
    return False

auth_result = supabase()
if auth_result:
    run_main_app()

# credentials = st.secrets["credentials"]

# authenticator = stauth.Authenticate(
#     credentials,
#     st.secrets["cookie_name"],
#     st.secrets["signature_key"],
#     cookie_expiry_days=1,
#     preauthorized=[]
# )

# st.title("BB PBP Analyser")

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status:
#     st.write(f"Welcome {name}")
#     run_main_app()
# elif authentication_status is False:
#     st.error("Username/password is incorrect")
# else:
# # elif authentication_status is None:
#     st.warning("Please enter your username and password")





        