

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
#     # If user already logged in, skip
#     if "user" in st.session_state:
#         st.success("Already logged in!")
#         return True

#     SUPABASE_URL = st.secrets["SUPABASE_URL"]
#     SUPABASE_ANON_KEY = st.secrets["SUPABASE_KEY"]
#     SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

#     # Create Supabase clients
#     supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
#     service_supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

#     st.title("Secure Login")

#     email = st.text_input("Enter your email address", key="email_input")

#     if st.button("Send OTP"):
#         if not email:
#             st.error("Please enter your email")
#         else:
#             try:
#                 resp = supabase.auth.sign_in_with_otp({"email": email})
#                 # sign_in_with_otp returns an AuthResponse object, no .error property; errors raise exceptions
#                 st.success("An OTP has been sent to your email.")
#             except Exception as e:
#                 st.error(f"Error sending OTP: {e}")

#     otp = st.text_input("Enter the OTP code", key="otp_input")

#     if st.button("Verify OTP"):
#         if not (email and otp):
#             st.error("Please enter both email and OTP")
#         else:
#             try:
#                 resp = supabase.auth.verify_otp({
#                     "email": email,
#                     "token": otp,
#                     "type": "email"
#                 })
#                 # resp is AuthResponse; extract session and user properly
#                 session = resp.session
#                 user = resp.user

#                 if session is None or user is None:
#                     st.error("OTP verification failed: no session or user returned.")
#                     return False

#                 user_email = user.email

#                 allowed_emails = st.secrets.get("allowed_emails", [])
#                 if user_email not in allowed_emails:
#                     st.error("You are not authorized to use this app.")
#                     return False

#                 # Insert login record with service key client to bypass RLS
#                 insert_resp = service_supabase.table("logins").insert({
#                     "email": user_email,
#                     "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
#                 }).execute()

#                 # Check for errors on insert
#                 # The execute() returns a PostgrestResponse; check status_code
#                 if insert_resp.error:
#                     st.warning(f"Warning: Could not log login time: {insert_resp.error.message}")

#                 st.success("You have successfully logged in!")
#                 st.session_state["user"] = user
#                 return True

#             except Exception as e:
#                 st.error(f"Error verifying OTP: {e}")

#     return False

def supabase():
    if "user" in st.session_state:
        st.success("Already logged in!")
        return True

    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_ANON_KEY = st.secrets["SUPABASE_KEY"]
    SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    service_supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    st.title("Secure Login")

    email = st.text_input("Enter your email address", key="email_input")

    if st.button("Send OTP"):
        if not email:
            st.error("Please enter your email")
        else:
            try:
                supabase.auth.sign_in_with_otp({"email": email})
                st.success("An OTP has been sent to your email.")
            except Exception as e:
                st.error(f"Error sending OTP: {e}")

    otp = st.text_input("Enter the OTP code", key="otp_input")

    if st.button("Verify OTP"):
        if not (email and otp):
            st.error("Please enter both email and OTP")
        else:
            try:
                resp = supabase.auth.verify_otp({
                    "email": email,
                    "token": otp,
                    "type": "email"
                })

                session = resp.session
                user = resp.user

                if session is None or user is None:
                    st.error("OTP verification failed: no session or user returned.")
                    return False

                user_email = user.email

                allowed_emails = st.secrets.get("allowed_emails", [])
                if user_email not in allowed_emails:
                    st.error("You are not authorized to use this app.")
                    return False

                # Insert login record using service client to bypass RLS
                insert_resp = service_supabase.table("logins").insert({
                    "email": user_email,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }).execute()

                if hasattr(insert_resp, "status_code") and insert_resp.status_code >= 400:
                    st.warning(f"Warning: Could not log login time: {insert_resp.data}")

                st.success("You have successfully logged in!")
                st.session_state["user"] = user
                return True

            except Exception as e:
                st.error(f"Error verifying OTP: {e}")

    return False

auth_result = supabase()
if auth_result:
    run_main_app()



        