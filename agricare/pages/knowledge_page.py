
import streamlit as st


def render_knowledge_page(user):

    st.markdown(
        '<div class="main-title">Knowledge Centre 📚</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Learn about potato diseases, prevention and better farming practices.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Disease knowledge database

    disease_data = {
        "Early Blight": {
            "cause": "Fungal disease caused by Alternaria solani.",
            "symptoms": [
                "Brown spots appear on older leaves.",
                "Spots may develop concentric ring patterns.",
                "Yellowing around affected areas.",
                "Severe infection can cause leaves to dry."
            ],
            "prevention": [
                "Use healthy and disease-free seed tubers.",
                "Remove infected plant debris.",
                "Maintain proper spacing between plants.",
                "Avoid unnecessary overhead irrigation.",
                "Follow crop rotation practices."
            ],
            "management": [
                "Inspect plants regularly for early symptoms.",
                "Remove severely infected leaves where practical.",
                "Use locally recommended fungicides only after consulting an agricultural expert."
            ]
        },

        "Late Blight": {
            "cause": "Disease caused by the oomycete Phytophthora infestans.",
            "symptoms": [
                "Water-soaked dark lesions on leaves.",
                "White fungal-like growth may appear on leaf undersides in humid conditions.",
                "Brown or black lesions can spread rapidly.",
                "Tubers may develop brown or reddish-brown rot."
            ],
            "prevention": [
                "Use certified disease-free seed tubers.",
                "Maintain good field drainage.",
                "Avoid excessive irrigation.",
                "Monitor crops during cool and humid weather.",
                "Remove infected plant material safely."
            ],
            "management": [
                "Inspect crops frequently during favourable weather.",
                "Remove and manage infected plants appropriately.",
                "Seek immediate local agricultural advice when symptoms appear.",
                "Use only officially recommended disease-control products."
            ]
        },

        "Healthy Potato Plant": {
            "cause": "No disease symptoms identified in the inspected plant.",
            "symptoms": [
                "Leaves are generally green.",
                "No obvious disease spots or lesions.",
                "Plant growth appears normal.",
                "No visible signs of severe infection."
            ],
            "prevention": [
                "Use quality seed tubers.",
                "Maintain balanced irrigation.",
                "Apply nutrients according to soil requirements.",
                "Monitor plants regularly.",
                "Follow crop rotation."
            ],
            "management": [
                "Continue regular crop inspection.",
                "Maintain suitable soil moisture.",
                "Remove weeds around plants.",
                "Monitor for new disease symptoms."
            ]
        }
    }

    # Search and filter

    search = st.text_input(
        "🔍 Search farming topics",
        placeholder="Search Early Blight, Late Blight, symptoms..."
    )

    selected_topic = st.selectbox(
        "Select a topic",
        list(disease_data.keys())
    )

    topic = disease_data[selected_topic]

    # Search matching

    if search.strip():

        searchable_text = (
            selected_topic + " " +
            topic["cause"] + " " +
            " ".join(topic["symptoms"]) + " " +
            " ".join(topic["prevention"]) + " " +
            " ".join(topic["management"])
        ).lower()

        if search.lower() not in searchable_text:
            st.warning("No matching information found in this topic.")
            return

    st.divider()

    st.subheader(f"🌱 {selected_topic}")

    st.markdown("### 🦠 Cause")
    st.write(topic["cause"])

    st.markdown("### 🔎 Symptoms")

    for symptom in topic["symptoms"]:
        st.write(f"• {symptom}")

    st.markdown("### 🛡️ Prevention")

    for point in topic["prevention"]:
        st.write(f"• {point}")

    st.markdown("### 💊 Management Guidance")

    for point in topic["management"]:
        st.write(f"• {point}")

    st.divider()

    st.subheader("🌾 General Potato Farming Tips")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**Irrigation**\n\n"
            "Maintain suitable soil moisture and avoid waterlogging."
        )

        st.info(
            "**Crop Rotation**\n\n"
            "Avoid repeatedly growing potatoes in the same field."
        )

    with col2:
        st.info(
            "**Soil Health**\n\n"
            "Use soil testing to guide fertilizer application."
        )

        st.info(
            "**Crop Monitoring**\n\n"
            "Inspect leaves and plants regularly for unusual symptoms."
        )

    st.warning(
        "This knowledge centre provides general educational guidance. "
        "Image-based disease predictions and visible symptoms are not "
        "a confirmed diagnosis. Consult a qualified agricultural expert "
        "before applying pesticides or fungicides."
    )
