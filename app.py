
import streamlit as st
import plotly.express as px
import pandas as pd

from agricare.pages.auth_page import render_auth_page
from agricare.pages.profile_page import render_profile_page
from agricare.pages.farms_page import render_farms_page
from agricare.pages.detection_page import render_detection_page

from agricare.pages.history_page import (
    render_history_page,
    render_analytics_page
)

from agricare.services.dashboard import get_dashboard_data

from agricare.pages.expenses_page import render_expenses_page

from agricare.pages.activities_page import render_activities_page

from agricare.pages.harvest_page import render_harvest_page

from agricare.pages.weather_page import render_weather_page

from agricare.pages.knowledge_page import render_knowledge_page

from agricare.pages.notifications_page import render_notifications_page

from agricare.pages.assistant_page import render_assistant_page


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AgriCare AI | Farmer Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------


st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F5F8F5;
    color: #24352B;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #173D2B;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

/* Main headings */
.main-title {
    font-size: 32px;
    font-weight: 750;
    color: #173D2B !important;
}

.subtitle {
    color: #52665A !important;
    font-size: 15px;
}

/* All headings */
h1, h2, h3, h4 {
    color: #173D2B !important;
}

/* General text */
.stApp p,
.stApp label,
.stApp span {
    color: #24352B;
}

/* Metric cards */
.metric-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE8DE;
}

.metric-label {
    color: #52665A !important;
    font-size: 14px;
}

.metric-value {
    color: #236B45 !important;
    font-size: 29px;
    font-weight: bold;
}

.metric-note {
    color: #687A6D !important;
    font-size: 12px;
}

/* Buttons */
.stButton > button {
    background-color: #236B45;
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #173D2B;
    color: #FFFFFF !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border-radius: 10px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF;
    color: #24352B !important;
}

/* Select boxes */
[data-baseweb="select"] * {
    color: #24352B !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# AUTHENTICATION CHECK
# -----------------------------------

if "user" not in st.session_state:

    render_auth_page()

    st.stop()

# -----------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------

with st.sidebar:

    st.markdown("## 🌱 AgriCare AI")
    st.caption("Smart Potato Farming Platform")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "My Profile",
            "My Farms",
            "Disease Detection",
            "Scan History",
            "Disease Analytics",
            "Weather & Crop Health",
            "Crop Activity Calendar",
            "Expense Tracker",
            "Yield & Harvest Management",
            "AI Farming Assistant",
            "Knowledge Centre",
            "Alerts & Notifications",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 👨‍🌾 Farmer Account")

current_user = st.session_state["user"]

st.markdown(f"**{current_user['full_name']}**")

location = ", ".join(
    filter(None, [
        current_user["district"],
        current_user["state"]
    ])
)

st.caption(location if location else "Location not provided")

if st.button("Logout", use_container_width=True):

    st.session_state.pop("user", None)

    st.rerun()

    st.caption("AgriCare AI v1.0")



# -----------------------------------
# DASHBOARD PAGE
# -----------------------------------

if page == "Dashboard":

    data = get_dashboard_data(current_user["id"])

    st.markdown(
        '<div class="main-title">Farmer Dashboard 🌱</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Welcome to your personalized farming overview.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        f"👨‍🌾 Welcome, {current_user['full_name']}! "
        "Here is your farm health overview."
    )

    # METRIC CARDS

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Registered Farms", str(data["total_farms"]), "Your registered farms"),
        ("Total Farm Area", f"{data['total_area']:.2f} Acres", "Combined area"),
        ("Total Leaf Scans", str(data["total_scans"]), "All-time scans"),
        ("Disease Detected", str(data["disease_scans"]), "Disease-positive scans")
    ]

    for col, metric in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{metric[0]}</div>
                    <div class="metric-value">{metric[1]}</div>
                    <div class="metric-note">{metric[2]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.divider()

    # ANALYTICS SECTION

    left, right = st.columns(2)

    with left:
        st.subheader("🌿 Disease Detection Overview")

        disease_data = pd.DataFrame({
            "Disease": ["Healthy", "Disease Detected"],
            "Scans": [
                data["healthy_scans"],
                data["disease_scans"]
            ]
        })

        if data["total_scans"] > 0:
            fig = px.pie(
                disease_data,
                names="Disease",
                values="Scans",
                hole=0.55,
                title="Distribution of Leaf Scan Results"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No leaf scans available yet.")

    with right:
        st.subheader("📊 Recent Scanning Activity")

        recent_scans = data["recent_scans"]

        if recent_scans:
            recent_data = pd.DataFrame([
                {
                    "Disease": {
                        "Potato___Early_blight": "Early Blight",
                        "Potato___Late_blight": "Late Blight",
                        "Potato___healthy": "Healthy"
                    }.get(scan["predicted_class"], scan["predicted_class"]),
                    "Confidence": f"{scan['confidence'] * 100:.2f}%",
                    "Date": scan["created_at"]
                }
                for scan in recent_scans
            ])

            st.dataframe(
                recent_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No recent scans found.")

    st.divider()

    # RECENT ACTIVITIES

    st.subheader("🕒 Recent Farm Activities")

    if recent_scans:
        activity_data = pd.DataFrame([
            {
                "Activity": "Potato leaf scanned",
                "Result": scan["predicted_class"].replace("Potato___", ""),
                "Date": scan["created_at"]
            }
            for scan in recent_scans
        ])

        st.dataframe(
            activity_data,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No farm activities recorded yet.")

    st.caption("Dashboard statistics are fetched from your actual farmer account.")


# -----------------------------------
# MY PROFILE PAGE
# -----------------------------------

elif page == "My Profile":

    current_user = st.session_state["user"]

    render_profile_page(current_user)

elif page == "My Farms":
    current_user = st.session_state["user"]
    render_farms_page(current_user)


elif page == "Disease Detection":
    current_user = st.session_state["user"]
    render_detection_page(current_user)

elif page == "Scan History":
    current_user = st.session_state["user"]
    render_history_page(current_user)

elif page == "Disease Analytics":
    current_user = st.session_state["user"]
    render_analytics_page(current_user)

elif page == "Expense Tracker":
    current_user = st.session_state["user"]
    render_expenses_page(current_user)

elif page == "Crop Activity Calendar":
    current_user = st.session_state["user"]
    render_activities_page(current_user)

elif page == "Yield & Harvest Management":
    current_user = st.session_state["user"]
    render_harvest_page(current_user)

elif page == "Weather & Crop Health":
    current_user = st.session_state["user"]
    render_weather_page(current_user)

elif page == "Knowledge Centre":
    current_user = st.session_state["user"]
    render_knowledge_page(current_user)

elif page == "Alerts & Notifications":
    current_user = st.session_state["user"]
    render_notifications_page(current_user)

elif page == "AI Farming Assistant":
    current_user = st.session_state["user"]
    render_assistant_page(current_user)




# -----------------------------------
# OTHER PAGE PLACEHOLDERS
# -----------------------------------

else:

    st.markdown(
        '<div class="main-title">🌱 ' + page + '</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"The {page} module will be implemented in the upcoming development phase."
    )