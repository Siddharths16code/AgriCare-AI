import io
import streamlit as st
import pandas as pd
from PIL import Image

from agricare.services.disease_detection import (
    predict_disease,
    save_scan
)
from agricare.services.farms import get_user_farms


DISEASE_NAMES = {
    "Potato___Early_blight": "Early Blight",
    "Potato___Late_blight": "Late Blight",
    "Potato___healthy": "Healthy Potato Leaf"
}


def render_detection_page(user):
    st.title("🔬 Potato Disease Detection")
    st.caption("Upload a potato leaf image for AI-powered analysis.")

    farms = get_user_farms(user["id"])

    selected_farm_id = None

    if farms:
        farm_options = {
            f["farm_name"]: f["id"] for f in farms
        }
        selected_farm = st.selectbox(
            "Select Farm (Optional)",
            ["Not linked to a farm"] + list(farm_options.keys())
        )

        if selected_farm != "Not linked to a farm":
            selected_farm_id = farm_options[selected_farm]
    else:
        st.info("You can add a farm later from the My Farms page.")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Potato Leaf Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(io.BytesIO(uploaded_file.getvalue())).convert("RGB")

        st.image(
            image,
            caption="Uploaded Potato Leaf",
            width=350
        )

        if st.button("🔍 Analyze Leaf", type="primary", use_container_width=True):
            with st.spinner("AI model is analyzing the leaf..."):
                try:
                    predicted_class, confidence, probabilities = predict_disease(image)

                    success, message = save_scan(
                        user_id=user["id"],
                        farm_id=selected_farm_id,
                        image=image,
                        predicted_class=predicted_class,
                        confidence=confidence,
                        probabilities=probabilities
                    )

                    st.session_state["latest_scan"] = {
                        "predicted_class": predicted_class,
                        "confidence": confidence,
                        "probabilities": probabilities,
                        "saved": success,
                        "message": message
                    }

                except Exception as error:
                    st.error(f"Detection failed: {error}")

    result = st.session_state.get("latest_scan")

    if result:
        st.divider()
        st.subheader("🧪 Detection Result")

        predicted_class = result["predicted_class"]
        friendly_name = DISEASE_NAMES.get(predicted_class, predicted_class)
        confidence = result["confidence"]

        if predicted_class == "Potato___healthy":
            st.success(f"Prediction: {friendly_name}")
        else:
            st.warning(f"Prediction: {friendly_name}")

        st.metric("Model Confidence", f"{confidence * 100:.2f}%")

        st.subheader("Class-wise Probabilities")

        chart_data = pd.DataFrame({
            "Disease": [
                DISEASE_NAMES.get(name, name)
                for name in result["probabilities"]
            ],
            "Probability (%)": [
                value * 100
                for value in result["probabilities"].values()
            ]
        })

        st.bar_chart(
            chart_data.set_index("Disease"),
            horizontal=True
        )

        if result["saved"]:
            st.success(result["message"])
        else:
            st.error(result["message"])

        st.caption(
            "This model recognizes only Early Blight, Late Blight and Healthy "
            "classes. It does not estimate disease severity. Confirm suspected "
            "disease with a qualified agricultural expert before treatment."
        )