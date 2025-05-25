

# 2025-05-23

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import tempfile
from zpbp_stage_one import generate_report

def run_main_app():
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


credentials = st.secrets["credentials"]

authenticator = stauth.Authenticate(
    credentials,
    st.secrets["cookie_name"],
    st.secrets["signature_key"],
    cookie_expiry_days=1,
    preauthorized=[]
)

st.title("BB PBP Analyser")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.write(f"Welcome {name}")
    run_main_app()
elif authentication_status is False:
    st.error("Username/password is incorrect")
else:
# elif authentication_status is None:
    st.warning("Please enter your username and password")





        