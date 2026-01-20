import streamlit as st
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import json

# -------------------- THEME (Black / White / Grey) --------------------
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

# -------------------- GOOGLE SHEETS AUTH --------------------
sa_info = json.loads(st.secrets["google_service_account"]["key"])

creds = Credentials.from_service_account_info(
    sa_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(creds)

# -------------------- CONNECT TO SHEET --------------------
SHEET_ID = "1fawsdd4TvuSbMRmczRtV_UtXE5Xe1YRM-jCR_UL80Rw"
WORKSHEET_NAME = "Transactions"

spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

# -------------------- HELPERS --------------------
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
    worksheet.append_row([
        date_str,
        t_type,
        main,
        sub,
        narration,
        amount,
        timestamp
    ])

# -------------------- APP UI --------------------
st.title("Edward Expense Tracker")
st.subheader(f"{indian_greeting()}, Edward Monthero!")

# Session defaults
if "amount_text" not in st.session_state:
    st.session_state.amount_text = ""

if "narration" not in st.session_state:
    st.session_state.narration = ""

# Transaction type
t_type = st.selectbox("Type", ["Income", "Expense"])

# Heads
main_heads = {
    "Income": ["Salary"],
    "Expense": [
        "Health & Fitness",
        "Groceries & Household",
        "Entertainment",
        "Transportation",
        "Debt Repayment",
        "Donations",
        "Investments",
        "Utilities",
        "Family Support"
    ]
}

sub_heads = {
    "Health & Fitness": ["Gym fee", "Protein"],
    "Groceries & Household": ["Fruits", "Soap, paste, shampoo"],
    "Entertainment": ["Netflix recharge", "Mastmaga news fees", "Movie ticket"],
    "Transportation": ["Bus ticket", "Auto charges"],
    "Debt Repayment": ["Credit card repayment", "Bank loan"],
    "Donations": ["Church offerings", "Other donation"],
    "Investments": ["KSFE chit fund", "Stock"],
    "Utilities": [
        "Mobile recharge (Self)",
        "Mobile recharge (Brother)",
        "Mobile recharge (Mother)"
    ],
    "Family Support": [
        "Money sent to Brother",
        "Money sent to Mother",
        "Family medicines (Mother/Brother)"
    ]
}

# Main & Sub
main = st.selectbox("Main Head", main_heads[t_type])
sub = st.selectbox("Sub Head", sub_heads.get(main, ["Other"]))

# Narration
narration = st.text_input("Narration (optional)", key="narration")

# Amount (blank by default)
amount_text = st.text_input("Amount", key="amount_text")

# -------------------- SAVE --------------------
if st.button("Save Transaction"):
    if amount_text.strip() == "":
        st.warning("Please enter amount")
    else:
        amount = float(amount_text)
        append_transaction(
            t_type,
            main,
            sub,
            narration or "-",
            amount
        )
        st.success("Transaction saved")

        # Clear inputs after save
        st.session_state.amount_text = ""
        st.session_state.narration = ""
