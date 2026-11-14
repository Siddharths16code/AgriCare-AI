
import streamlit as st
import pandas as pd
from datetime import date

from agricare.services.farms import (
    add_farm,
    get_user_farms,
    delete_farm
)


def render_farms_page(user):

    st.title("🌾 My Farms")
    st.caption("Register and manage your potato farms.")

    user_id = user["id"]

    farms = get_user_farms(user_id)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Registered Farms", len(farms))

    with col2:
        total_area = sum(float(f["area_acres"]) for f in farms)
        st.metric("Total Farm Area", f"{total_area:.2f} Acres")

    st.divider()

    with st.expander("➕ Register a New Farm", expanded=not farms):

        with st.form("add_farm_form"):

            farm_name = st.text_input("Farm Name")
            area = st.number_input(
                "Farm Area (Acres)",
                min_value=0.1,
                max_value=100000.0,
                value=1.0,
                step=0.1
            )

            soil = st.selectbox(
                "Soil Type",
                ["Sandy", "Loamy", "Clay", "Silty", "Other"]
            )

            irrigation = st.selectbox(
                "Irrigation Method",
                ["Drip", "Sprinkler", "Flood", "Rainfed", "Other"]
            )

            variety = st.text_input(
                "Potato Variety",
                placeholder="e.g. Kufri Jyoti"
            )

            sowing_date = st.date_input(
                "Sowing Date",
                value=date.today()
            )

            stage = st.selectbox(
                "Crop Growth Stage",
                [
                    "Land Preparation",
                    "Planting",
                    "Vegetative Growth",
                    "Tuber Formation",
                    "Tuber Bulking",
                    "Maturity",
                    "Harvested"
                ]
            )

            submitted = st.form_submit_button(
                "Save Farm",
                use_container_width=True
            )

        if submitted:

            success, message = add_farm(
                user_id=user_id,
                farm_name=farm_name,
                area_acres=area,
                soil_type=soil,
                irrigation_method=irrigation,
                potato_variety=variety,
                sowing_date=sowing_date.isoformat(),
                crop_stage=stage
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()
    st.subheader("Your Registered Farms")

    if farms:

        display_data = []

        for farm in farms:
            display_data.append({
                "Farm Name": farm["farm_name"],
                "Area (Acres)": farm["area_acres"],
                "Soil": farm["soil_type"],
                "Irrigation": farm["irrigation_method"],
                "Potato Variety": farm["potato_variety"],
                "Sowing Date": farm["sowing_date"],
                "Crop Stage": farm["crop_stage"]
            })

        st.dataframe(
            pd.DataFrame(display_data),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Delete a Farm")

        farm_options = {
            f"{farm['farm_name']} (ID: {farm['id']})": farm["id"]
            for farm in farms
        }

        selected_farm = st.selectbox(
            "Select farm",
            list(farm_options.keys())
        )

        if st.button("🗑️ Delete Selected Farm"):

            success, message = delete_farm(
                user_id,
                farm_options[selected_farm]
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    else:
        st.info("No farms registered yet. Add your first farm above.")
