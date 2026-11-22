# ==========================================================
# PERSONAL EXPENSE TRACKER
# Login + Signup + Expense Management
# ==========================================================

# 1. IMPORT LIBRARIES

import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import base64
from pathlib import Path


# 2. PAGE CONFIGURATION

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💜",
    layout="wide"
)


# 3. FILE PATHS

DB_NAME = "expenses.db"

BG_IMAGE = Path("background.png")

if not BG_IMAGE.exists():
    BG_IMAGE = Path("Background.png")


# 4. DATABASE CREATION

def create_database():

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


create_database()


# 5. PASSWORD HASHING

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# 6. BACKGROUND IMAGE

if BG_IMAGE.exists():

    with open(BG_IMAGE, "rb") as image_file:

        image_data = base64.b64encode(
            image_file.read()
        ).decode()

    background_style = f"""
        background-image:
        linear-gradient(
            rgba(15, 10, 15, 0.55),
            rgba(15, 10, 15, 0.72)
        ),
        url("data:image/png;base64,{image_data}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """

else:

    background_style = "background: #171019;"


# 7. CUSTOM CSS

st.markdown(f"""
<style>

/* Hide Streamlit Header */

header[data-testid="stHeader"] {{
    display: none !important;
}}

div[data-testid="stToolbar"] {{
    display: none !important;
}}

div[data-testid="stDecoration"] {{
    display: none !important;
}}

#MainMenu {{
    visibility: hidden;
}}

/* Full Page Background */

.stApp {{
    {background_style}
}}

div[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}

div[data-testid="stMain"] {{
    background: transparent !important;
}}

section.main {{
    background: transparent !important;
}}

section.main > div {{
    padding-top: 1rem !important;
}}

/* Headings */

h1, h2, h3 {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
    opacity: 1 !important;
    text-shadow: 2px 2px 8px #000000;
}}

/* Paragraph */

.stMarkdown p {{
    color: #F5F0FF !important;
    text-shadow: 1px 1px 4px #000000;
}}

/* Login Signup Card */

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(30, 20, 38, 0.82) !important;
    border: 1px solid rgba(210, 165, 255, 0.55) !important;
    border-radius: 20px !important;
    padding: 18px !important;
    box-shadow: 0 0 25px rgba(150,70,220,0.30);
    backdrop-filter: blur(10px);
}}

/* Input Labels */

label {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* Input Boxes */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {{
    background-color: #38283F !important;
    color: #FFFFFF !important;
    border: 1px solid #B58ACD !important;
    border-radius: 10px !important;
}}

.stTextInput input:focus,
.stNumberInput input:focus {{
    border: 1px solid #D9A5FF !important;
    box-shadow: 0 0 8px rgba(217,165,255,0.5);
}}

/* Select Box */

.stSelectbox div[data-baseweb="select"] > div {{
    background-color: #38283F !important;
    color: #FFFFFF !important;
    border: 1px solid #B58ACD !important;
    border-radius: 10px !important;
}}

/* Buttons */

.stButton button,
.stFormSubmitButton button {{
    background-color: #287A55 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}}

/* Button Hover */

.stButton button:hover,
.stFormSubmitButton button:hover {{
    background-color: #9655C7 !important;
    color: white !important;
    box-shadow: 0 0 15px rgba(190,120,255,0.5);
}}

/* Tabs */

.stTabs [data-baseweb="tab"] {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

.stTabs [aria-selected="true"] {{
    color: #E2B8FF !important;
}}

/* Radio and Checkbox */

.stRadio label,
.stCheckbox label {{
    color: #FFFFFF !important;
}}

/* Metric Cards */

div[data-testid="stMetric"] {{
    background: rgba(55,35,65,0.88) !important;
    padding: 18px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(190,130,255,0.35);
}}

div[data-testid="stMetricLabel"] {{
    color: #E5D1F5 !important;
}}

div[data-testid="stMetricValue"] {{
    color: #FFFFFF !important;
}}

/* Dataframe */

div[data-testid="stDataFrame"] {{
    background-color: rgba(30,20,35,0.9);
    border-radius: 12px;
}}

/* Divider */

hr {{
    border-color: #A477B8 !important;
}}

/* Footer */

footer {{
    visibility: hidden;
}}

</style>
""", unsafe_allow_html=True)


# 8. SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""


# 9. LOGIN AND SIGNUP PAGE

if not st.session_state.logged_in:

    st.markdown("""
        <h1 style="
            text-align:center;
            color:#FFFFFF;
            font-size:38px;
            font-weight:800;
            text-shadow:2px 2px 10px #000000;
        ">
            💰 Personal Expense Tracker
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p style="
            text-align:center;
            color:#FFFFFF;
            font-size:17px;
            font-weight:600;
            text-shadow:1px 1px 5px #000000;
        ">
            Manage your money. Track your expenses.
        </p>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([1, 1.4, 1])

    with middle:

        with st.container(border=True):

            st.markdown("""
                <h2 style="
                    text-align:center;
                    color:#FFFFFF;
                    font-weight:800;
                    text-shadow:2px 2px 8px #000000;
                ">
                    Welcome
                </h2>
            """, unsafe_allow_html=True)

            login_tab, signup_tab = st.tabs(
                ["🔐 Login", "📝 Sign Up"]
            )

            # LOGIN SECTION

            with login_tab:

                st.subheader("Login to your account")

                login_username = st.text_input(
                    "Username",
                    key="login_username"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )

                if st.button("Login", use_container_width=True):

                    if login_username and login_password:

                        with sqlite3.connect(DB_NAME) as conn:

                            result = conn.execute("""
                                SELECT id, username
                                FROM users
                                WHERE username = ?
                                AND password = ?
                            """, (
                                login_username,
                                hash_password(login_password)
                            )).fetchone()

                        if result:

                            st.session_state.logged_in = True
                            st.session_state.user_id = result[0]
                            st.session_state.username = result[1]

                            st.success("Login successful!")

                            st.rerun()

                        else:

                            st.error(
                                "Invalid username or password."
                            )

                    else:

                        st.warning(
                            "Please enter username and password."
                        )

            # SIGNUP SECTION

            with signup_tab:

                st.subheader("Create a new account")

                signup_username = st.text_input(
                    "Choose Username",
                    key="signup_username"
                )

                signup_password = st.text_input(
                    "Create Password",
                    type="password",
                    key="signup_password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    key="confirm_password"
                )

                if st.button(
                    "Create Account",
                    use_container_width=True
                ):

                    if not signup_username or not signup_password:

                        st.warning(
                            "Please fill all required fields."
                        )

                    elif len(signup_password) < 6:

                        st.warning(
                            "Password must be at least 6 characters."
                        )

                    elif signup_password != confirm_password:

                        st.error(
                            "Passwords do not match."
                        )

                    else:

                        try:

                            with sqlite3.connect(DB_NAME) as conn:

                                conn.execute("""
                                    INSERT INTO users
                                    (username, password)
                                    VALUES (?, ?)
                                """, (
                                    signup_username,
                                    hash_password(signup_password)
                                ))

                            st.success(
                                "Account created! Now login."
                            )

                        except sqlite3.IntegrityError:

                            st.error(
                                "Username already exists. Try another."
                            )
# ==========================================================
# 10. EXPENSE TRACKER DASHBOARD
# ==========================================================

else:

    # Welcome Heading

    st.title("💰 Personal Expense Tracker")

    st.write(
        f"Welcome, **{st.session_state.username}**!"
    )

    # Logout Button

    if st.button("Logout 🚪"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""

        st.rerun()

    st.divider()


    # ======================================================
    # 11. ADD NEW EXPENSE
    # ======================================================

    st.subheader("➕ Add New Expense")

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Health",
                "Other"
            ]
        )

        description = st.text_input(
            "Description"
        )

        expense_date = st.date_input(
            "Expense Date"
        )

        submit_expense = st.form_submit_button(
            "Add Expense"
        )

        if submit_expense:

            if amount <= 0:

                st.warning(
                    "Please enter an amount greater than zero."
                )

            else:

                with sqlite3.connect(DB_NAME) as conn:

                    conn.execute("""
                        INSERT INTO expenses
                        (
                            user_id,
                            amount,
                            category,
                            description,
                            expense_date
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        st.session_state.user_id,
                        amount,
                        category,
                        description,
                        str(expense_date)
                    ))

                st.success(
                    "Expense added successfully! 🎉"
                )

                st.rerun()


    st.divider()


    # ======================================================
    # 12. FETCH CURRENT USER EXPENSES
    # ======================================================

    with sqlite3.connect(DB_NAME) as conn:

        rows = conn.execute("""
            SELECT
                id,
                amount,
                category,
                description,
                expense_date
            FROM expenses
            WHERE user_id = ?
            ORDER BY expense_date DESC, id DESC
        """, (
            st.session_state.user_id,
        )).fetchall()


    # ======================================================
    # 13. CONVERT DATA INTO DATAFRAME
    # ======================================================

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ]
    )


    # ======================================================
    # 14. EXPENSE SUMMARY
    # ======================================================

    st.subheader("📊 Expense Summary")

    if not df.empty:

        total_expense = df["Amount"].sum()
        total_count = len(df)

    else:

        total_expense = 0
        total_count = 0

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💸 Total Expenses",
            f"₹{total_expense:,.2f}"
        )

    with col2:

        st.metric(
            "📝 Number of Expenses",
            total_count
        )


    st.divider()


    # ======================================================
    # 15. CATEGORY-WISE CHART
    # ======================================================

    st.subheader("📈 Category-wise Spending")

    if not df.empty:

        category_totals = (
            df.groupby("Category")["Amount"].sum()
        )

        st.bar_chart(category_totals)

    else:

        st.info(
            "Add expenses to see your chart."
        )


    st.divider()


    # ======================================================
    # 16. EXPENSE HISTORY
    # ======================================================

    st.subheader("📋 Expense History")

    if not df.empty:

        display_df = df.drop(
            columns=["ID"]
        ).rename(columns={
            "Amount": "Amount (₹)",
            "Date": "Expense Date"
        })

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        # ==================================================
        # 17. DELETE EXPENSE
        # ==================================================

        st.subheader("🗑️ Delete an Expense")

        expense_options = {
            (
                f"₹{row[1]:,.2f} | "
                f"{row[2]} | "
                f"{row[4]} | "
                f"{row[3] or 'No description'}"
            ): row[0]
            for row in rows
        }

        selected_expense = st.selectbox(
            "Choose an expense to delete",
            list(expense_options.keys())
        )

        if st.button("Delete Selected Expense 🗑️"):

            selected_id = expense_options[
                selected_expense
            ]

            with sqlite3.connect(DB_NAME) as conn:

                conn.execute("""
                    DELETE FROM expenses
                    WHERE id = ? AND user_id = ?
                """, (
                    selected_id,
                    st.session_state.user_id
                ))

            st.success(
                "Expense deleted successfully!"
            )

            st.rerun()

    else:

        st.info(
            "No expenses added yet. Add your first expense!"
        )


    # ======================================================
    # 18. FOOTER
    # ======================================================

    st.divider()

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#E2B8FF;
            font-weight:600;
            text-shadow:1px 1px 4px #000000;
        ">
            💜 Track Smart • Save More • Grow More
        </p>
        """,
        unsafe_allow_html=True
    )                            