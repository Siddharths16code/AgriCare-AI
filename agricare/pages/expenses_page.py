
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from agricare.services.expenses import (
    add_expense,
    get_user_expenses,
    get_expense_summary,
    delete_expense
)
from agricare.services.farms import get_user_farms


def render_expenses_page(user):

    st.markdown(
        '<div class="main-title">Farm Expense Tracker 💰</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Track and manage your farming expenses.</div>',
        unsafe_allow_html=True
    )

    user_id = user["id"]

    # Fetch existing records
    expenses = get_user_expenses(user_id)
    summary = get_expense_summary(user_id)

    # Expense summary
    total = summary["total_expenses"]
    expense_count = len(expenses)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Expenditure", f"₹{total:,.2f}")

    with col2:
        st.metric("Total Expense Records", expense_count)

    st.divider()

    # Add expense
    st.subheader("➕ Add New Expense")

    farms = get_user_farms(user_id)

    farm_options = {"No specific farm": None}
    for farm in farms:
        farm_options[farm["farm_name"]] = farm["id"]

    with st.form("add_expense_form"):

        selected_farm = st.selectbox(
            "Select Farm",
            list(farm_options.keys())
        )

        category = st.selectbox(
            "Expense Category",
            [
                "Seeds",
                "Fertilizers",
                "Pesticides",
                "Labour",
                "Irrigation",
                "Machinery",
                "Transportation",
                "Other"
            ]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=1.0,
            step=100.0
        )

        description = st.text_area(
            "Description",
            placeholder="Enter expense details..."
        )

        expense_date = st.date_input(
            "Expense Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Save Expense",
            use_container_width=True
        )

        if submitted:

            success, message = add_expense(
                user_id,
                farm_options[selected_farm],
                category,
                amount,
                description,
                expense_date.isoformat()
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # Category-wise analytics
    st.subheader("📊 Category-wise Expense Analysis")

    category_data = summary["category_breakdown"]

    if category_data:

        df_category = pd.DataFrame(category_data)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                df_category,
                names="category",
                values="total_amount",
                hole=0.5,
                title="Expense Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                df_category,
                x="category",
                y="total_amount",
                title="Category-wise Spending",
                labels={
                    "category": "Category",
                    "total_amount": "Amount (₹)"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No expense data available yet.")

    st.divider()

    # Expense history
    st.subheader("📋 Expense History")

    if expenses:

        df = pd.DataFrame(expenses)

        display_df = df[
            [
                "id",
                "farm_name",
                "category",
                "amount",
                "description",
                "expense_date"
            ]
        ].copy()

        display_df.columns = [
            "ID",
            "Farm",
            "Category",
            "Amount (₹)",
            "Description",
            "Date"
        ]

        display_df["Farm"] = display_df["Farm"].fillna("Not linked")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗑️ Delete Expense")

        expense_options = {
            f"#{item['id']} | {item['category']} | ₹{item['amount']:.2f} | {item['expense_date']}": item["id"]
            for item in expenses
        }

        selected_expense = st.selectbox(
            "Select expense to delete",
            list(expense_options.keys())
        )

        if st.button("Delete Selected Expense", type="secondary"):

            success, message = delete_expense(
                user_id,
                expense_options[selected_expense]
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    else:
        st.info("You have not added any expenses yet.")
