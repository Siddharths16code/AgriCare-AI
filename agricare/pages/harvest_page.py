
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from agricare.services.harvest import (
    add_harvest,
    get_harvest_records,
    get_harvest_summary,
    delete_harvest_record
)
from agricare.services.farms import get_user_farms


def render_harvest_page(user):

    st.markdown(
        '<div class="main-title">Yield & Harvest Management 🌾</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Track your potato production and harvest revenue.</div>',
        unsafe_allow_html=True
    )

    user_id = user["id"]

    records = get_harvest_records(user_id)
    summary = get_harvest_summary(user_id)

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Production",
        f"{summary['total_quantity']:,.2f} kg"
    )

    col2.metric(
        "Total Revenue",
        f"₹{summary['total_revenue']:,.2f}"
    )

    col3.metric(
        "Harvest Records",
        summary["total_records"]
    )

    st.divider()

    # Add harvest record
    st.subheader("➕ Add Harvest Record")

    farms = get_user_farms(user_id)

    farm_options = {
        farm["farm_name"]: farm
        for farm in farms
    }

    if not farms:
        st.warning("Please register a farm in My Farms before adding a harvest record.")

    with st.form("harvest_form"):

        selected_farm = st.selectbox(
            "Select Farm",
            list(farm_options.keys()) if farms else ["No farm available"]
        )

        harvest_date = st.date_input(
            "Harvest Date",
            value=date.today()
        )

        quantity = st.number_input(
            "Harvest Quantity (kg)",
            min_value=0.1,
            step=10.0
        )

        selling_price = st.number_input(
            "Selling Price (₹ per kg)",
            min_value=0.0,
            step=1.0
        )

        notes = st.text_area(
            "Additional Notes",
            placeholder="Enter harvest details..."
        )

        submitted = st.form_submit_button(
            "Save Harvest Record",
            use_container_width=True,
            disabled=not farms
        )

        if submitted:

            success, message = add_harvest(
                user_id,
                farm_options[selected_farm]["id"],
                harvest_date.isoformat(),
                quantity,
                selling_price,
                notes
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # Production analysis
    st.subheader("📊 Production Analysis")

    if records:

        df = pd.DataFrame(records)

        farm_production = (
            df.groupby("farm_name", dropna=False)["quantity_kg"]
            .sum()
            .reset_index()
        )

        farm_production["farm_name"] = (
            farm_production["farm_name"].fillna("Not linked")
        )

        fig = px.bar(
            farm_production,
            x="farm_name",
            y="quantity_kg",
            title="Farm-wise Potato Production",
            labels={
                "farm_name": "Farm",
                "quantity_kg": "Production (kg)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        # Yield per acre for linked farms
        linked_records = df[
            df["area_acres"].notna() & (df["area_acres"] > 0)
        ]

        if not linked_records.empty:

            st.subheader("🌱 Yield per Acre")

            farm_yield = (
                linked_records.groupby(
                    ["farm_name", "area_acres"],
                    as_index=False
                )["quantity_kg"].sum()
            )

            farm_yield["Yield (kg/acre)"] = (
                farm_yield["quantity_kg"] / farm_yield["area_acres"]
            )

            st.dataframe(
                farm_yield[
                    ["farm_name", "area_acres", "quantity_kg", "Yield (kg/acre)"]
                ].rename(columns={
                    "farm_name": "Farm",
                    "area_acres": "Area (Acres)",
                    "quantity_kg": "Production (kg)"
                }),
                use_container_width=True,
                hide_index=True
            )

    else:
        st.info("Add harvest records to view production analytics.")

    st.divider()

    # Harvest history
    st.subheader("📋 Harvest History")

    if records:

        display_df = pd.DataFrame(records)[
            [
                "id",
                "farm_name",
                "harvest_date",
                "quantity_kg",
                "selling_price",
                "notes"
            ]
        ].copy()

        display_df.columns = [
            "ID",
            "Farm",
            "Harvest Date",
            "Quantity (kg)",
            "Price (₹/kg)",
            "Notes"
        ]

        display_df["Farm"] = display_df["Farm"].fillna("Not linked")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗑️ Delete Harvest Record")

        record_options = {
            f"#{r['id']} | {r['farm_name'] or 'Not linked'} | {r['quantity_kg']} kg": r["id"]
            for r in records
        }

        selected_record = st.selectbox(
            "Select record",
            list(record_options.keys())
        )

        if st.button("Delete Selected Record"):

            success, message = delete_harvest_record(
                user_id,
                record_options[selected_record]
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    else:
        st.info("No harvest records available yet.")
