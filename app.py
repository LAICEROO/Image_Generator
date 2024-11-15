import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import requests
import io

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Hugging Face API Configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to query the Hugging Face model for image generation
def query_image_generation(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content  # Returns the image bytes
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# Function to display an image in Streamlit
def display_image_from_bytes(image_bytes, caption="Generated Image"):
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption=caption, use_container_width=True)

# Streamlit App Layout
st.title("Chat  ")

# Sidebar for Navigation
st.sidebar.title("Options")
choice = st.sidebar.radio("Select an Option", ["Text Generation", "Image Generation"])

# Image Generation Section
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None

if choice == "Text Generation":
    st.header("Text Generation")
    user_prompt = st.text_area("Write your question here")

elif choice == "Image Generation":
    st.header("Image Generation - Stable Diffusion")
    user_prompt = st.text_area("Describe the image you want to generate:")

    if st.button("Generate Image"):
        if user_prompt.strip():
            generated_image_bytes = query_image_generation(user_prompt)
            if generated_image_bytes:
                st.session_state.generated_image_bytes = generated_image_bytes  # Save to session state
                image = Image.open(io.BytesIO(generated_image_bytes))
                st.image(image, caption="Generated Image", use_container_width=True)
        else:
            st.warning("Please enter a description to generate an image.")

    if st.button("Download Generated Image"):
        if st.session_state.generated_image_bytes:  # Retrieve from session state
            image = Image.open(io.BytesIO(st.session_state.generated_image_bytes))
            image.save("generated_image.png")
            st.success("Image saved as generated_image.png")
        else:
            st.warning("No image to save. Please generate an image first.")