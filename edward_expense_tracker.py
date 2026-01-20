import streamlit as st
st.title("💰 Edward Expense Tracker")
st.subheader(f"{indian_greeting()} 👋")

# Maintain selected main head
if "main" not in st.session_state:
    st.session_state.main = "Health & Fitness"

t_type = st.selectbox("Type", ["Income", "Expense"], key="type_select")

main_heads = {
    "Income": ["Salary", "Other"],
    "Expense": ["Health & Fitness", "Groceries & Household", "Entertainment",
                "Transportation", "Debt Repayment", "Donations", "Utilities", "Family Support"]
}

sub_heads = {
    "Health & Fitness": ["Gym fee", "Protein"],
    "Groceries & Household": ["Fruits", "Soap, paste, shampoo"],
    "Entertainment": ["Netflix recharge", "Mastmaga news fees", "Movie ticket"],
    "Transportation": ["Bus ticket", "Auto charges"],
    "Debt Repayment": ["Credit card repayment", "Bank loan"],
    "Donations": ["Church offerings", "Other donation"],
    "Utilities": ["Mobile recharge (Self)", "Mobile recharge (Brother)", "Mobile recharge (Mother)"],
    "Family Support": ["Money sent to Brother", "Money sent to Mother", "Family medicines (Mother/Brother)"]
}

# Dynamic main head selectbox
main = st.selectbox("Main Head", main_heads[t_type], key="main_select",
                    on_change=lambda: st.session_state.update({"sub": None}))

# Dynamic sub head selectbox based on main
sub_options = sub_heads.get(main, ["Other"])
sub = st.selectbox("Sub Head", sub_options, key="sub_select")

# Other inputs
narration = st.text_input("Narration (optional)", key="narration")
amount = st.number_input("Amount", min_value=0.0, step=1.0, key="amount")

# Save button outside the form for instant reactivity
if st.button("Save Transaction"):
    append_transaction(t_type, main, sub, narration or "-", amount)
    st.success("✅ Transaction saved!")
    # Reset inputs
    st.session_state.update({"narration": "", "amount": 0.0, "main_select": main, "sub_select": sub_options[0]})
