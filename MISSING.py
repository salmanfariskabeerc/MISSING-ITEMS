import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Missing Items System", layout="wide")

# ==========================================
# GOOGLE SHEETS SETUP
# ==========================================
SHEET_URL = "YOUR_GOOGLE_SHEET_URL"
MISSING_SHEET_NAME = "MissingItems"

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"], scopes=scope
    )

    client = gspread.authorize(creds)
    sh = client.open_by_url(SHEET_URL)
    missing_worksheet = sh.worksheet(MISSING_SHEET_NAME)

    sheets_connected = True
except Exception as e:
    st.error(f"Google Sheets Error: {e}")
    sheets_connected = False


# ==========================================
# LOGIN
# ==========================================
outlets = [
    "Hilal", "Safa Super", "Azhar HP", "Azhar",
    "Blue Pearl", "Fida", "Hadeqat", "Jais",
    "Sabah", "Sahat", "Shams salem",
    "Shams Liwan", "Superstore",
    "Tay Tay", "Safa oudmehta",
    "Port saeed", "Logistics Warehouse"
]

PASSWORD = "123123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Missing Items Login")

    username = st.text_input("Username")
    outlet = st.selectbox("Select Outlet", outlets)
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "almadina" and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.outlet = outlet
            st.rerun()
        else:
            st.error("Invalid login")

# ==========================================
# MAIN APP
# ==========================================
else:

    st.title(f"📦 Missing Items - {st.session_state.outlet}")

    staff_name = st.text_input("👤 Staff Name (Required)")

    st.markdown("---")

    barcode = st.text_input("Barcode")
    item_name = st.text_input("Item Name")
    supplier = st.text_input("Supplier")
    qty = st.number_input("Missing Quantity", min_value=1, step=1)
    remarks = st.text_area("Remarks (Optional)")

    if st.button("➕ Add Missing Item", type="primary"):

        if not staff_name.strip():
            st.error("Staff Name is required")
        elif not barcode.strip():
            st.error("Barcode is required")
        elif not item_name.strip():
            st.error("Item Name is required")
        else:

            new_row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.outlet,
                staff_name,
                barcode,
                item_name,
                supplier,
                qty,
                remarks
            ]

            if sheets_connected:
                try:
                    # Add headers if empty
                    if not missing_worksheet.row_values(1):
                        missing_worksheet.append_row([
                            "Date",
                            "Outlet",
                            "Staff Name",
                            "Barcode",
                            "Item Name",
                            "Supplier",
                            "Missing Qty",
                            "Remarks"
                        ])

                    missing_worksheet.append_row(new_row)
                    st.success("✅ Missing item recorded successfully")
                except Exception as e:
                    st.error(f"Upload error: {e}")
            else:
                st.error("Google Sheets not connected")
