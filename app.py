import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

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
            st.success("Image captured successfully!")
else:
    # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")
st.divider()

col1, col2 = st.columns(2)

# Input 2: Select the social media platform
col1.subheader("Select the Social Media Platform 🌐")
social_media_platform = col1.selectbox(
    "Select the Social Media Platform",
    ["Instagram", "Facebook", "Twitter", "LinkedIn", "Pinterest"],
)
col1.divider()

# Input 3: Creativity Level (Temperature)
col2.subheader("Creativity Level 🪄")
creativity = col2.radio(
    "How creative do you want the captions to be?",
    ('Low', 'Medium', 'High')
)
col2.divider()

# Input 4: Emoji Usage
col1.subheader("Emoji Usage 😎")
emoji_usage = col1.radio("Do you want to use emojis in the captions?", ('Yes', 'No'))
col1.divider()

# Input 5: Hashtags
col2.subheader("Hashtags '#'")
hashtags = col2.radio("Do you want to include hashtags in the captions?", ('Yes', 'No'))
col2.divider()

# Input 6: Size of the captions
col1.subheader("Caption Length 📏")
caption_length = col1.slider("Select the length of the captions", min_value=50, max_value=400, value=200, step=50)

# Input 7: Number of Captions user wants
col2.subheader("Number of Captions 7️⃣")
num_captions = col2.slider("Select the number of captions", min_value=1, max_value=5, value=2)

st.divider()

# Input 8: User Input Prompts
st.subheader("User Input Prompt 🖊️")
user_input_prompts = st.text_area("Enter the description or prompt for the image")
st.divider()

# Generate Captions
if st.button("Generate Captions"):
    if uploaded_file is None:
        st.warning("Please upload an image or capture one.")

    else:
        # Define prebuild prompts
        complete_prompt = f'''{user_input_prompts}. Generate {num_captions} captions for the image, for "{social_media_platform}" platform.
        Analyse the image and generate creative captions for my social media post. Maintain the captions creativity level as "{creativity}". 
        Give a short, bold and little large title for each caption. You need to use trending hashtags? Answer is strictly "{hashtags}". You 
        need to use Emojies for the post? Answer is strictly "{emoji_usage}". (IMPORTANT) Use {caption_length} words for each caption 
        strictly, but just remember that, when we give the caption length, then make caption {caption_length} words long (excluding hashtags)
        and give hashtags (if user asked) after making the caption as long as user want. The cation should be related to {social_media_platform} 
        platform. Maintain the space between each caption, so that user can able to read the captions more clearly. (IMPORTANT) First write
        "Generated Captions" as Heading, then give caption number (in next line), then caption title (in next line) and then the caption,
        NOTE: FOLLOW THIS INSTRUCTION FOR EACH AND EVERY CAPTIONS.'''

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

## Footer ##
st.markdown("---")
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <div style="text-align:center;">
        <p>Made with ❤️ by Anubhav Yadav</p>
        <p>Follow me on 
            <a href="https://linkedin.com/in/anubhav-yadav-srm" target="_blank"><i class="fab fa-linkedin"></i>LinkedIn</a> | 
            <a href="https://github.com/AnubhavYadavBCA25" target="_blank"><i class="fab fa-github"></i>GitHub</a> |
            <a href="https://sites.google.com/view/anubhavyadavportfolio" target="_blank"><i class="fas fa-globe"></i>Portfolio Website</a>
        </p>
    </div>
    """, unsafe_allow_html=True
)