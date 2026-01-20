import streamlit as st
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import json

# ---------- Theme: Black, White & Grey ----------
st.markdown(
    """
    <style>
    .stApp { background-color: #f5f5f5; color: #000000; }
    .stButton>button { background-color: #ffffff; color: #000000; border: 1px solid #888888; }
    .stTextInput>div>input { background-color: #ffffff; color: #000000; border: 1px solid #888888; }
    .stSelectbox>div>div>div { background-color: #ffffff; color: #000000; border: 1px solid #888888; }
    .stSuccess { background-color: #dddddd !important; color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Google Sheets Authentication ----------
sa_info = json.loads(st.secrets["google_service_account"]["key"])
creds = Credentials.from_service_account_info(
    sa_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(creds)

# ---------- Connect to Google Sheet ----------
SHEET_ID = "1fawsdd4TvuSbMRmczRtV_UtXE5Xe1YRM-jCR_UL80Rw"
worksheet_name = "Transactions"
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(worksheet_name)

# ---------- Helper Functions ----------
def indian_greeting():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    hour = now.hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def append_transaction(t_type, main, sub, narration, amount):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([date_str, t_type, main, sub, narration, amount, timestamp])

# ---------- Initialise session_state defaults ----------
if "t_type" not in st.session_state:
    st.session_state.t_type = "Expense"
if "main" not in st.session_state:
    st.session_state.main = "Health & Fitness"
if "sub" not in st.session_state:
    st.session_state.sub = ""
if "narration" not in st.session_state:
    st.session_state.narration = ""
if "amount_text" not in st.session_state:
    st.session_state.amount_text = ""

# ---------- Streamlit App ----------
st.title("Edward Expense Tracker")
st.subheader(f"{indian_greeting()}")

# Main heads & subheads
main_heads = {
    "Income": ["Salary", "Other"],
    "Expense": ["Health & Fitness", "Groceries & Household", "Entertainment",
                "Transportation", "Debt Repayment", "Donations", "Investments", "Utilities", "Family Support"]
}

sub_heads = {
    "Health & Fitness": ["Gym fee", "Protein"],
    "Groceries & Household": ["Fruits", "Soap, paste, shampoo"],
    "Entertainment": ["Netflix recharge", "Mastmaga news fees", "Movie ticket"],
    "Transportation": ["Bus ticket", "Auto charges"],
    "Debt Repayment": ["Credit card repayment", "Bank loan"],
    "Donations": ["Church offerings", "Other donation"],
    "Investments": ["KSFE chit fund", "Stock"],
    "Utilities": ["Mobile recharge (Self)", "Mobile recharge (Brother)", "Mobile recharge (Mother)"],
    "Family Support": ["Money sent to Brother", "Money sent to Mother", "Family medicines (Mother/Brother)"]
}

# Transaction type (bind to session_state)
t_type = st.selectbox(
    "Type",
    ["Income", "Expense"],
    key="t_type",
)

# Dynamic main head (bind to session_state)
main = st.selectbox(
    "Main Head",
    main_heads[t_type],
    key="main",
)

# Dynamic subhead (bind to session_state)
sub_options = sub_heads.get(main, ["Other"])
# IMPORTANT: give default value from session_state if present, else first option
if st.session_state.sub not in sub_options:
    st.session_state.sub = sub_options[0]

sub = st.selectbox(
    "Sub Head",
    sub_options,
    key="sub",
)

# Narration
narration = st.text_input(
    "Narration (optional)",
    key="narration",
)

# Amount input (blank by default)
amount_text = st.text_input(
    "Amount",
    value=st.session_state.amount_text,
    key="amount_text",
)

# Save button
if st.button("Save Transaction"):
    amt_value = float(amount_text) if amount_text.strip() else 0.0
    append_transaction(t_type, main, sub, narration or "-", amt_value)

    # RESET ALL FIELDS HERE
    st.session_state.t_type = "Expense"
    st.session_state.main = "Health & Fitness"
    st.session_state.sub = ""          # will be corrected to first option on next run
    st.session_state.narration = ""
    st.session_state.amount_text = ""

    st.success("Transaction saved!")
