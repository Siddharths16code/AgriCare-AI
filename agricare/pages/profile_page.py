
import streamlit as st

from agricare.services.profile import (
    get_user_profile,
    update_user_profile
)


def render_profile_page(user):

    profile = get_user_profile(user["id"])

    if not profile:
        st.error("Farmer profile could not be found.")
        return

    st.title("👨‍🌾 My Profile")
    st.caption("View and manage your personal farming account details.")

    st.divider()

    # Account information
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Personal Information")

    with col2:
        st.markdown("### Account Details")

    st.info(f"Farmer ID: {profile['id']}")

    with st.form("profile_update_form"):

        st.subheader("Personal Details")

        full_name = st.text_input(
            "Full Name",
            value=profile["full_name"] or ""
        )

        email = st.text_input(
            "Email Address",
            value=profile["email"] or "",
            disabled=True
        )

        phone = st.text_input(
            "Phone Number",
            value=profile["phone"] or ""
        )

        st.divider()

        st.subheader("Location Details")

        village = st.text_input(
            "Village",
            value=profile["village"] or ""
        )

        district = st.text_input(
            "District",
            value=profile["district"] or ""
        )

        state = st.text_input(
            "State",
            value=profile["state"] or ""
        )

        languages = ["English", "Hindi"]

        current_language = profile["preferred_language"]

        language_index = (
            languages.index(current_language)
            if current_language in languages
            else 0
        )

        preferred_language = st.selectbox(
            "Preferred Language",
            languages,
            index=language_index
        )

        st.divider()

        save_button = st.form_submit_button(
            "💾 Save Profile Changes",
            use_container_width=True
        )

    if save_button:

        success, message = update_user_profile(
            user_id=profile["id"],
            full_name=full_name,
            phone=phone,
            village=village,
            district=district,
            state=state,
            preferred_language=preferred_language
        )

        if success:

            updated_profile = get_user_profile(profile["id"])

            st.session_state["user"] = updated_profile
            st.session_state["profile_message"] = message

            st.rerun()

        else:
            st.error(message)

    if "profile_message" in st.session_state:

        st.success(st.session_state.pop("profile_message"))

    st.divider()

    st.subheader("Account Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Farmer Account ID",
            profile["id"]
        )

    with col2:
        st.metric(
            "Account Created",
            str(profile["created_at"])[:10]
            if profile["created_at"]
            else "Not available"
        )
