import streamlit as st
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

# Set up the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Model selection
model = genai.GenerativeModel("gemini-pro-vision")

st.header("🤖 CapBot: AI-Powered Caption Generator", divider="rainbow")

# Input 1: Upload the image or Use the camera to capture an image
# Upload or Capture Image
st.subheader("Upload Image or Capture Image with Webcam")

# Upload the image
st.write("Upload an image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

st.subheader("OR")

# Caputre the image
st.write("Capture an image...")
if uploaded_file is None:
    st.write("Please use the camera to capture one.")
    use_camera = st.checkbox("Use Camera")
    if use_camera:
        captured_image = st.camera_input("Capture an image")
        if captured_image:
            uploaded_file = captured_image
            st.success("Image captured successfully!")
else:
    # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")
st.divider()

# Input 2: Select the social media platform
st.subheader("Select the Social Media Platform")
social_media_platform = st.selectbox(
    "Select the Social Media Platform",
    ["Instagram", "Facebook", "Twitter", "LinkedIn", "Pinterest"],
)
st.divider()

# Input 3: Creativity Level (Temperature)
st.subheader("Creativity Level")
creativity = st.radio(
    "How creative do you want the captions to be?",
    ('Low', 'Medium', 'High')
)
# Map creativity level to temperature
creativity_map = {
    'Low':0.5,
    'Medium':0.75,
    'High':1.0
}
temperature = creativity_map[creativity]
st.divider()

# Input 4: Number of Captions user wants
st.subheader("Number of Captions")
num_captions = st.slider("Select the number of captions", min_value=1, max_value=10, value=5)
st.divider()