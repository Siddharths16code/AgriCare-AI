
import streamlit as st
import pandas as pd
from datetime import date, timedelta

from agricare.services.activities import get_user_activities
from agricare.services.weather import (
    get_weather,
    get_crop_recommendations
)


def render_notifications_page(user):

    st.markdown(
        '<div class="main-title">Alerts & Notifications 🔔</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Stay updated with your farm activities and weather risks.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Fetch farmer activities

    activities = get_user_activities(user["id"])

    today = date.today()
    upcoming_limit = today + timedelta(days=7)

    overdue = []
    due_today = []
    upcoming = []

    for activity in activities:

        if activity["status"] == "Completed":
            continue

        activity_date = pd.to_datetime(
            activity["scheduled_date"]
        ).date()

        if activity_date < today:
            overdue.append(activity)

        elif activity_date == today:
            due_today.append(activity)

        elif today < activity_date <= upcoming_limit:
            upcoming.append(activity)

    # Alert summary

    col1, col2, col3 = st.columns(3)

    col1.metric("Overdue", len(overdue))
    col2.metric("Due Today", len(due_today))
    col3.metric("Upcoming (7 Days)", len(upcoming))

    st.divider()

    # Overdue activities

    st.subheader("🚨 Overdue Activities")

    if overdue:

        for activity in overdue:

            st.error(
                f"**{activity['activity_name']}**\n\n"
                f"Scheduled: {activity['scheduled_date']}\n\n"
                f"Farm: {activity.get('farm_name') or 'Not linked'}"
            )

    else:
        st.success("No overdue farming activities!")

    # Today's activities

    st.subheader("📅 Activities Due Today")

    if due_today:

        for activity in due_today:

            st.warning(
                f"**{activity['activity_name']}**\n\n"
                f"Farm: {activity.get('farm_name') or 'Not linked'}"
            )

    else:
        st.info("No activities scheduled for today.")

    # Upcoming activities

    st.subheader("🌱 Upcoming Activities")

    if upcoming:

        for activity in upcoming:

            st.info(
                f"**{activity['activity_name']}**\n\n"
                f"Scheduled: {activity['scheduled_date']}\n\n"
                f"Farm: {activity.get('farm_name') or 'Not linked'}"
            )

    else:
        st.info("No upcoming activities in the next 7 days.")

    st.divider()

    # Weather alerts

    st.subheader("🌦️ Weather-Based Alerts")

    city = st.text_input(
        "Enter your farming location",
        value="Sonipat",
        key="notification_weather_city"
    )

    if st.button("Check Weather Alerts"):

        if not city.strip():
            st.warning("Please enter a location.")
        else:

            with st.spinner("Checking weather conditions..."):

                weather, error = get_weather(city.strip())

            if error:
                st.error(error)

            else:

                recommendations = get_crop_recommendations(weather)

                st.session_state["notification_weather"] = {
                    "location": weather["location"]["name"],
                    "recommendations": recommendations
                }

    weather_alert = st.session_state.get(
        "notification_weather"
    )

    if weather_alert:

        st.write(
            f"Location: **{weather_alert['location']}**"
        )

        for recommendation in weather_alert["recommendations"]:
            st.warning(f"🌿 {recommendation}")

    st.caption(
        "These are in-app informational alerts. "
        "They do not send SMS or push notifications."
    )
