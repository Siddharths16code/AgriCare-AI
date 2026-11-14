
import streamlit as st
import pandas as pd
from datetime import date

from agricare.services.activities import (
    add_activity,
    get_user_activities,
    update_activity_status,
    delete_activity
)
from agricare.services.farms import get_user_farms


def render_activities_page(user):

    st.markdown(
        '<div class="main-title">Crop Activity Calendar 🌱</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Schedule and manage your farming activities.</div>',
        unsafe_allow_html=True
    )

    user_id = user["id"]

    activities = get_user_activities(user_id)

    # Activity statistics
    total = len(activities)
    completed = sum(1 for a in activities if a["status"] == "Completed")
    pending = total - completed

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Activities", total)
    col2.metric("Pending", pending)
    col3.metric("Completed", completed)

    st.divider()

    # Add new activity
    st.subheader("➕ Schedule New Activity")

    farms = get_user_farms(user_id)

    farm_options = {"No specific farm": None}

    for farm in farms:
        farm_options[farm["farm_name"]] = farm["id"]

    activity_types = [
        "Land Preparation",
        "Sowing",
        "Irrigation",
        "Fertilizer Application",
        "Pesticide Spraying",
        "Weed Removal",
        "Crop Inspection",
        "Harvesting",
        "Other"
    ]

    with st.form("add_activity_form"):

        selected_farm = st.selectbox(
            "Select Farm",
            list(farm_options.keys())
        )

        activity_name = st.selectbox(
            "Activity Type",
            activity_types
        )

        description = st.text_area(
            "Activity Description",
            placeholder="Enter activity details..."
        )

        scheduled_date = st.date_input(
            "Scheduled Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Schedule Activity",
            use_container_width=True
        )

        if submitted:

            success, message = add_activity(
                user_id,
                farm_options[selected_farm],
                activity_name,
                description,
                scheduled_date.isoformat()
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # Activity list
    st.subheader("📅 Your Farming Schedule")

    if activities:

        for activity in activities:

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**{activity['activity_name']}**")

                    st.write(
                        f"📅 Date: {activity['scheduled_date'] or 'Not specified'}"
                    )

                    st.write(
                        f"🚜 Farm: {activity['farm_name'] or 'Not linked'}"
                    )

                    if activity["description"]:
                        st.caption(activity["description"])

                with col2:
                    if activity["status"] == "Completed":
                        st.success("Completed")
                    else:
                        st.warning("Pending")

                    new_status = st.selectbox(
                        "Status",
                        ["Pending", "Completed"],
                        index=0 if activity["status"] == "Pending" else 1,
                        key=f"status_{activity['id']}"
                    )

                    if new_status != activity["status"]:
                        success, message = update_activity_status(
                            user_id,
                            activity["id"],
                            new_status
                        )

                        if success:
                            st.rerun()
                        else:
                            st.error(message)

                    if st.button(
                        "Delete",
                        key=f"delete_{activity['id']}"
                    ):
                        success, message = delete_activity(
                            user_id,
                            activity["id"]
                        )

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

    else:
        st.info("No farming activities scheduled yet.")

    st.divider()

    # Calendar view
    st.subheader("🗓️ Calendar Overview")

    dated_activities = [
        a for a in activities if a["scheduled_date"]
    ]

    if dated_activities:

        calendar_df = pd.DataFrame(dated_activities)

        calendar_df = calendar_df[
            ["scheduled_date", "activity_name", "farm_name", "status"]
        ].copy()

        calendar_df.columns = [
            "Date", "Activity", "Farm", "Status"
        ]

        st.dataframe(
            calendar_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Your scheduled activities will appear here.")
