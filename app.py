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
# This must be the first Streamlit command.

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# 3. FILE PATHS

DB_NAME = "expenses.db"
BG_IMAGE = Path("background.png")


# 4. DATABASE CONNECTION AND TABLE CREATION

def create_database():

    with sqlite3.connect(DB_NAME) as conn:

        # Users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Expenses table
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


# 6. BACKGROUND IMAGE AND CUSTOM CSS

if BG_IMAGE.exists():

    with open(BG_IMAGE, "rb") as image_file:

        image_data = base64.b64encode(
            image_file.read()
        ).decode()

    background_style = f"""
        background-image:
        linear-gradient(
            rgba(15, 10, 15, 0.68),
            rgba(15, 10, 15, 0.78)
        ),
        url("data:image/png;base64,{image_data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    """

else:

    background_style = "background: #171019;"


st.markdown(f"""
<style>

/* Main background */

.stApp {{
    {background_style}
}}

/* Main text */

h1, h2, h3, p, label {{
    color: #ffffff;
}}

/* Login and signup card */

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(35, 24, 39, 0.90);
    border: 1px solid rgba(190, 130, 255, 0.35);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 0 20px rgba(150, 70, 220, 0.18);
}}

/* Input boxes */

.stTextInput input,
.stNumberInput input,
.stDateInput input {{
    background-color: #38283b !important;
    color: white !important;
    border: 1px solid #8b5aa8 !important;
    border-radius: 9px !important;
}}

/* Select boxes */

.stSelectbox div[data-baseweb="select"] > div {{
    background-color: #38283b;
    color: white;
    border: 1px solid #8b5aa8;
    border-radius: 9px;
}}

/* Buttons */

.stButton button,
.stFormSubmitButton button {{
    background-color: #287a55;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 9px 20px;
    font-weight: bold;
    transition: 0.3s;
}}

/* Button hover */

.stButton button:hover,
.stFormSubmitButton button:hover {{
    background-color: #9655c7;
    color: white;
    border: none;
}}

/* Radio buttons */

.stRadio label {{
    color: white !important;
}}

/* Checkbox */

.stCheckbox label {{
    color: white !important;
}}

/* Dataframe */

div[data-testid="stDataFrame"] {{
    background-color: rgba(30, 20, 35, 0.9);
    border-radius: 12px;
}}

/* Tabs */

.stTabs [data-baseweb="tab"] {{
    color: white;
}}

.stTabs [aria-selected="true"] {{
    color: #d9a5ff !important;
}}

/* Metric cards */

div[data-testid="stMetric"] {{
    background: rgba(55, 35, 60, 0.85);
    padding: 15px;
    border-radius: 12px;
}}

/* Divider */

hr {{
    border-color: #80558f;
}}

</style>
""", unsafe_allow_html=True)


# 7. SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""


# 8. LOGIN AND SIGNUP PAGE

if not st.session_state.logged_in:

    st.markdown(
        "<h1 style='text-align:center;'>💰 Expense Tracker</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Manage your money. Track your expenses."
        "</p>",
        unsafe_allow_html=True
    )

    # Center login card

    left, middle, right = st.columns(
        [1, 1.4, 1]
    )

    with middle:

        with st.container(border=True):

            st.markdown(
                "<h2 style='text-align:center;'>Welcome</h2>",
                unsafe_allow_html=True
            )

            # Login / Signup tabs

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

                if st.button(
                    "Login",
                    use_container_width=True
                ):

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


# 9. EXPENSE TRACKER DASHBOARD

else:

    # Welcome heading

    st.title("💰 Personal Expense Tracker")

    st.write(
        f"Welcome, **{st.session_state.username}**!"
    )

    # Logout button

    if st.button("Logout 🚪"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""

        st.rerun()

    st.divider()


    # 10. ADD NEW EXPENSE

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


    # 11. FETCH CURRENT USER EXPENSES

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


    # 12. CONVERT DATA INTO DATAFRAME

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


    # 13. SUMMARY

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


    # 14. CATEGORY-WISE CHART

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


    # 15. EXPENSE HISTORY

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


        # 16. DELETE EXPENSE

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


    # 17. FOOTER

    st.divider()

    st.markdown(
        """
        <p style="text-align:center; color:#d9a5ff;">
            💜 Track Smart • Save More • Grow More
        </p>
        """,
        unsafe_allow_html=True
    )