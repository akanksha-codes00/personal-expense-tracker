
import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💜",
    layout="wide"
)

DB_NAME = "expenses.db"

# ---------------- DATABASE SETUP ----------------
def setup_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL
            )
        """)

setup_database()

# ---------------- CUSTOM DESIGN ----------------
# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>

.stApp,
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #121116 0%,
        #1B1922 55%,
        #24212D 100%
    ) !important;
    color: #F3EEF8 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

h1, h2, h3 {
    color: #D6C2F5 !important;
}

p, label {
    color: #E6DFEF !important;
}

div[data-testid="stMetric"] {
    background: #8B6B52 !important;
    border-color:#B89A7D !important;
    border: 1px solid #40344F !important;
    border-radius: 18px;
    padding: 22px;
}

div[data-testid="stForm"] {
    background: #1D1B24 !important;
    border: 1px solid #40344F !important;
    border-radius: 18px;
    padding: 24px;
}

hr {
    border-color: #40344F !important;
}
h1, h2, h3 {
    color: #E5C3A2 !important;
    font-weight: 750 !important;
}

p, label {
    color: #F0E5D8 !important;
}


div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #78977A, #7651A8) !important;
    color: #FFFFFF !important;
    border: 1px solid #9CB69A !important;
    border-radius: 12px !important;
    min-height: 44px;
    font-weight: 650;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #91AD91, #78977A) !important;
    color: #C06C91 !important;
    border: 1px solid #B6CCB2 !important;
    transform: translateY(-2px);
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #C49A75 !important;
    color: #332923 !important;
}

div[data-testid="stMetric"] {
    background: #49382F !important;
    border: 1px solid #80634F;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.12);
}

div[data-testid="stMetricLabel"] {
    color: #D7BDA6 !important;
}

div[data-testid="stMetricValue"] {
    color: #F0D1AE !important;
    font-weight: 800;
}

div[data-testid="stForm"] {
    background: #3D3028 !important;
    border: 1px solid #80634F;
    border-radius: 18px;
    padding: 24px;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #F0E5D8 !important;
    border-radius: 10px;
    border-color: #C49A75 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #80634F;
    border-radius: 14px;
    overflow: hidden;
}

hr {
    border-color: #80634F;
}
</style>
""", unsafe_allow_html=True)
# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- LOGIN / SIGNUP PAGE ----------------
if not st.session_state.logged_in:

    st.title("💜 Welcome to Expense Tracker")
    st.write("Your money, your records, your control.")
    st.divider()

    left, center, right = st.columns([1, 2, 1])

    with center:
        choice = st.radio(
            "Choose an option",
            ["Login", "Sign Up"],
            horizontal=True
        )

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if choice == "Sign Up":
            if st.button("Create Account", use_container_width=True):
                if not username.strip() or not password:
                    st.warning("Enter username and password.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    hashed_password = hashlib.sha256(
                        password.encode()
                    ).hexdigest()

                    try:
                        with sqlite3.connect(DB_NAME) as conn:
                            conn.execute(
                                """INSERT INTO users (username, password)
                                   VALUES (?, ?)""",
                                (username.strip(), hashed_password)
                            )
                        st.success("Account created! Now select Login.")
                    except sqlite3.IntegrityError:
                        st.error("This username already exists.")

        else:
            if st.button("Login", use_container_width=True):
                if not username.strip() or not password:
                    st.warning("Enter username and password.")
                else:
                    hashed_password = hashlib.sha256(
                        password.encode()
                    ).hexdigest()

                    with sqlite3.connect(DB_NAME) as conn:
                        user = conn.execute(
                            """SELECT id, username FROM users
                               WHERE username = ? AND password = ?""",
                            (username.strip(), hashed_password)
                        ).fetchone()

                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

# ---------------- EXPENSE DASHBOARD ----------------
else:
    st.title("💜 Personal Expense Tracker")
    st.write(f"Welcome, {st.session_state.username}!")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()

    st.divider()

    # Load only the current user's expenses
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            """SELECT id, amount, category, description, expense_date
               FROM expenses
               WHERE user_id = ?
               ORDER BY expense_date DESC, id DESC""",
            (st.session_state.user_id,)
        ).fetchall()

    df = pd.DataFrame(
        rows,
        columns=["ID", "Amount", "Category", "Description", "Date"]
    )

    # ---------------- ADD EXPENSE ----------------
    st.subheader("➕ Add a New Expense")

    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping", "Education",
             "Bills", "Health", "Other"]
        )

        description = st.text_input("Description")
        expense_date = st.date_input("Expense Date")

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if amount <= 0:
                st.warning("Enter an amount greater than zero.")
            else:
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute(
                        """INSERT INTO expenses
                           (user_id, amount, category, description, expense_date)
                           VALUES (?, ?, ?, ?, ?)""",
                        (
                            st.session_state.user_id,
                            amount,
                            category,
                            description.strip(),
                            str(expense_date)
                        )
                    )

                st.success("Expense added successfully!")
                st.rerun()

    st.divider()

    # ---------------- SUMMARY ----------------
    st.subheader("📊 Expense Summary")

    total = float(df["Amount"].sum()) if not df.empty else 0
    count = len(df)

    col1, col2 = st.columns(2)
    col1.metric("Total Expenses", f"₹{total:,.2f}")
    col2.metric("Number of Expenses", count)

    # ---------------- CATEGORY CHART ----------------
    if not df.empty:
        st.subheader("📈 Category-wise Spending")
        category_totals = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_totals)

    # ---------------- EXPENSE HISTORY ----------------
    st.subheader("📋 Expense History")

    if not df.empty:
        display_df = df.drop(columns=["ID"]).rename(
            columns={
                "Amount": "Amount (₹)",
                "Date": "Expense Date"
            }
        )
        st.dataframe(display_df, use_container_width=True)

        # ---------------- DELETE EXPENSE ----------------
        st.subheader("🗑️ Delete an Expense")

        expense_options = {
            f"₹{row[1]:,.2f} | {row[2]} | {row[4]} | {row[3]}": row[0]
            for row in rows
        }

        selected_expense = st.selectbox(
            "Choose an expense to delete",
            list(expense_options.keys())
        )

        if st.button("Delete Selected Expense"):
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute(
                    "DELETE FROM expenses WHERE id = ? AND user_id = ?",
                    (
                        expense_options[selected_expense],
                        st.session_state.user_id
                    )
                )
            st.success("Expense deleted.")
            st.rerun()

    else:
        st.info("No expenses added yet. Add your first expense above!")