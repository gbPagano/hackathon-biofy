import streamlit as st
import httpx


st.title("Pathogenic Finder")
files = st.file_uploader(
    "Selecione Imagens para Predição",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True,
)


def predict(img):
    url = "https://hackathon-biofy.fly.dev/predict"
    headers = {
        "accept": "application/json",
    }

    files = {
        "file": ("file.jpg", img, "image/jpeg"),
    }

    with httpx.Client() as client:
        response = client.post(url, headers=headers, files=files)
        return response.json()


if files is not None:
    with st.spinner("Wait for it..."):
        for img in files:
            st.text(f"Filename: {img.name}")
            result = predict(img)["result"]
            st.text(f"Prediction: {result}")
            st.image(img)
