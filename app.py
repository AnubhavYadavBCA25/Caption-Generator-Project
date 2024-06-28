import streamlit as st
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
from IPython.display import Markdown
import textwrap

load_dotenv()

# Function to convert text to markdown
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Set up the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Model selection
model = genai.GenerativeModel("gemini-1.5-flash")

## Streamlit App ##

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
            # uploaded_file_bytes = uploaded_file.read()
            # uploaded_file = Image.open(io.BytesIO(uploaded_file_bytes))

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


# Input 5: User Input Prompts
st.subheader("User Input Prompts")
user_input_prompts = st.text_area("Enter the description or prompts for the image")
st.divider()

# Generate Captions
if st.button("Generate Captions"):
    if uploaded_file is None:
        st.warning("Please upload an image or capture one.")

    else:
        st.write("Generating Captions...")

        # Define prebuild prompts
        complete_prompt = f'''{user_input_prompts}. Generate {num_captions} captions for the image for {social_media_platform} platform.
        Analyse the image and generate creative captions for my social media post. Use some trending hashtags for the post. Don't give too
        large captions. Keeps it short and simple. The image is related to {social_media_platform} platform.'''

        # Convert uploaded image to bytes
        image = Image.open(uploaded_file)

        # Generate captions using gemini model
        response = model.generate_content([complete_prompt,image],stream=True)
        response.resolve()

        # Ensure response is not None and has attribute 'text' before accessing it
        if response is not None:  # Check if response exists
            captions = response.text  # Access text data only if response is valid
            st.write(captions)
            st.success("Captions generated successfully!")
        else:
            st.error("Error: Failed to generate captions. Please try again.")
        