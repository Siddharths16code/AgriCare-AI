
import streamlit as st

from agricare.services.auth import (
    register_user,
    authenticate_user
)


def render_auth_page():

    st.markdown(
        "<h1 style='text-align:center;color:#173D2B;'>🌱 AgriCare AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Smart Potato Farming & Disease Management System</p>",
        unsafe_allow_html=True
    )

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        login_tab, register_tab = st.tabs(
            ["🔐 Login", "📝 Register"]
        )

        # -------------------------
        # LOGIN
        # -------------------------

        with login_tab:

            st.subheader("Farmer Login")

            with st.form("login_form"):

                email = st.text_input(
                    "Email Address",
                    placeholder="Enter your registered email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

            if login_button:

                if not email or not password:
                    st.error("Please enter email and password.")

                else:
                    user = authenticate_user(email, password)

                    if user:

                        st.session_state["user"] = user

                        st.success("Login successful!")

                        st.rerun()

                    else:
                        st.error("Invalid email or password.")

        # -------------------------
        # REGISTRATION
        # -------------------------

        with register_tab:

            st.subheader("Create Farmer Account")

            with st.form("registration_form"):

                full_name = st.text_input("Full Name")

                email = st.text_input("Email Address")

                phone = st.text_input("Phone Number")

                password = st.text_input(
                    "Create Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                st.markdown("#### Location Details")

                village = st.text_input("Village")

                district = st.text_input("District")

                state = st.text_input("State")

                language = st.selectbox(
                    "Preferred Language",
                    ["English", "Hindi"]
                )

                register_button = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

            if register_button:

                if not all([
                    full_name,
                    email,
                    phone,
                    password,
                    confirm_password
                ]):
                    st.error("Please fill all required fields.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                else:

                    success, message, user_id = register_user(
                        full_name=full_name,
                        email=email,
                        phone=phone,
                        password=password,
                        village=village,
                        district=district,
                        state=state,
                        preferred_language=language
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Your account has been created. "
                            "Please login using your credentials."
                        )

                    else:
                        st.error(message)
