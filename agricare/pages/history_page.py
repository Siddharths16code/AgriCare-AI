import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

from agricare.services.scan_history import (
    get_scan_history,
    get_scan_analytics
)

DISEASE_NAMES = {
    "Potato___Early_blight": "Early Blight",
    "Potato___Late_blight": "Late Blight",
    "Potato___healthy": "Healthy"
}


def render_history_page(user):

    st.title("📋 Disease Scan History")
    st.caption("View your previous potato leaf scans.")

    scans = get_scan_history(user["id"])

    total = len(scans)
    healthy = sum(
        1 for s in scans
        if s["predicted_class"] == "Potato___healthy"
    )
    infected = total - healthy

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", total)
    c2.metric("Healthy Scans", healthy)
    c3.metric("Disease Detected", infected)

    st.divider()
    st.subheader("Your Previous Scans")

    if not scans:
        st.info("No scan history available. Analyze your first potato leaf.")
        return

    for scan in scans:

        disease = DISEASE_NAMES.get(
            scan["predicted_class"],
            scan["predicted_class"]
        )

        with st.expander(
            f"Scan #{scan['id']} | {disease} | "
            f"{scan['confidence'] * 100:.2f}%"
        ):

            col1, col2 = st.columns([1, 2])

            with col1:
                image_path = scan["image_path"]

                if image_path and Path(image_path).exists():
                    st.image(
                        Image.open(image_path),
                        use_container_width=True
                    )
                else:
                    st.warning("Original image not found.")

            with col2:
                st.write(f"**Disease:** {disease}")
                st.write(
                    f"**Confidence:** {scan['confidence'] * 100:.2f}%"
                )
                st.write(
                    f"**Farm:** {scan['farm_name'] or 'Not linked'}"
                )
                st.write(f"**Date:** {scan['created_at']}")

                if scan["probabilities_json"]:
                    import json

                    probabilities = json.loads(
                        scan["probabilities_json"]
                    )

                    chart = pd.DataFrame({
                        "Class": [
                            DISEASE_NAMES.get(k, k)
                            for k in probabilities
                        ],
                        "Probability (%)": [
                            v * 100 for v in probabilities.values()
                        ]
                    })

                    st.bar_chart(
                        chart.set_index("Class"),
                        horizontal=True
                    )


def render_analytics_page(user):

    st.title("📊 Disease Analytics")
    st.caption("Understand disease patterns across your scans.")

    analytics = get_scan_analytics(user["id"])

    if not analytics:
        st.info("No scan data available yet.")
        return

    data = []

    for row in analytics:
        data.append({
            "Disease": DISEASE_NAMES.get(
                row["predicted_class"],
                row["predicted_class"]
            ),
            "Total Scans": row["total"]
        })

    df = pd.DataFrame(data)

    total = int(df["Total Scans"].sum())

    c1, c2 = st.columns(2)
    c1.metric("Total Scans", total)
    c2.metric("Disease Categories", len(df))

    st.divider()

    st.subheader("Disease Distribution")

    st.bar_chart(
        df.set_index("Disease"),
        horizontal=True
    )

    st.subheader("Scan Distribution")

    st.plotly_chart(
        __import__("plotly.express").express.pie(
            df,
            names="Disease",
            values="Total Scans",
            hole=0.45
        ),
        use_container_width=True
    )