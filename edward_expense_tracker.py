import streamlit as st
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import json

# ---------------- THEME ----------------
# ---------------- THEME ----------------
st.markdown(
    """
    <style>
    .stApp { 
        background-color: #f5f5f5; 
        color: #000000; 
    }
    .stButton>button { 
        background-color: #ffffff; 
        color: #000000; 
        border: 1px solid #888888; 
    }
    .stTextInput>div>input { 
        background-color: #ffffff; 
        color: #000000; 
        border: 1px solid #888888; 
    }
    .stSelectbox>div>div>div { 
        background-color: #ffffff; 
        color: #000000; 
        border: 1px solid #888888; 
    }
    .stSuccess { 
        background-color: #dddddd !important; 
        color: #000000 !important; 
    }
    
    /* Make all Streamlit labels/headings black */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #000000 !important;
    }
    
    /* Label styling for all form elements */
    [data-testid="stForm"] label,
    [data-testid="column"] label,
    .stSelectbox label,
    .stTextInput label {
        color: #000000 !important;
        font-weight: 500;
    }
    
    /* Widget labels specifically */
    div[data-testid="stHorizontalBlock"] > div > label,
    div.element-container > div > label {
        color: #000000 !important;
    }
    
    /* Title and subheader */
    .stMarkdown > h1,
    .stMarkdown > h2 {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- GOOGLE SHEETS AUTH ----------------
sa_info = json.loads(st.secrets["google_service_account"]["key"])
creds = Credentials.from_service_account_info(
    sa_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(creds)

SHEET_ID = "1fawsdd4TvuSbMRmczRtV_UtXE5Xe1YRM-jCR_UL80Rw"
spreadsheet = gc.open_by_key(SHEET_ID)

txn_ws = spreadsheet.worksheet("Transactions")
heads_ws = spreadsheet.worksheet("Heads")

# ---------------- HELPER FUNCTIONS ----------------
def indian_greeting():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    if now.hour < 12:
        return "Good morning"
    elif now.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def append_transaction(t_type, main, sub, narration, amount):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    txn_ws.append_row([
        now.strftime("%Y-%m-%d"),
        t_type,
        main,
        sub,
        narration,
        amount,
        now.strftime("%Y-%m-%d %H:%M:%S")
    ])

# ---------------- READ HEADS SHEET ----------------
data = heads_ws.get_all_values()

types_row = data[0]  # Row 1 = Type (Income/Expense)
main_row = data[1]   # Row 2 = Main heads
sub_rows = data[2:]  # Row 3+ = Sub categories

heads = {}
for col in range(len(main_row)):
    t = types_row[col].strip()
    main = main_row[col].strip()
    if not t or not main:
        continue

    subs = []
    for r in sub_rows:
        if col < len(r) and r[col].strip():
            subs.append(r[col].strip())

    heads.setdefault(t, {})[main] = subs or ["Other"]

# ---------------- STREAMLIT UI ----------------
st.title("Edward Expense Tracker")
st.subheader(f"{indian_greeting()}, Edward Monthero!!")

if "amount_text" not in st.session_state:
    st.session_state.amount_text = ""
if "narration" not in st.session_state:
    st.session_state.narration = ""

# Type selectbox
t_type = st.selectbox("Type", ["Income", "Expense"])

# Main head selectbox
main_options = list(heads.get(t_type, {}).keys())
main = st.selectbox("Main Head", main_options)

# Sub head selectbox
sub_options = heads[t_type][main]
sub = st.selectbox("Sub Head", sub_options)

# Narration input
narration = st.text_input("Narration (optional)", key="narration")

# Amount input (blank by default)
amount_text = st.text_input("Amount", key="amount_text")

# Save transaction button
if st.button("Save Transaction"):
    if not amount_text.strip():
        st.warning("Please enter amount")
    else:
        append_transaction(
            t_type,
            main,
            sub,
            narration or "-",
            float(amount_text)
        )
        st.success("Transaction saved!")

        # Clear inputs
        st.session_state.narration = ""
        st.session_state.amount_text = ""
