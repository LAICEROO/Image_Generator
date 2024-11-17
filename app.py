import os
from dotenv import load_dotenv  # Library to load environment variables from a .env file
import streamlit as st  # Streamlit for creating the user interface
from PIL import Image  # PIL (Pillow) for image handling
import requests  # Requests for making HTTP API calls
import io  # Module io for handling byte streams

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")  # Retrieve the API key from the environment file

# Configuration for the Hugging Face API for Stable Diffusion
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {API_KEY}"}  # Authorization headers

# Function to send a request to the Stable Diffusion model
def query_image_generation(prompt):
    # Send a POST request with the image description as input
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content  # Return the image bytes on success
    else:
        # Handle errors
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# Function to display an image in the Streamlit app
def display_image_from_bytes(image_bytes, caption="Generated Image"):
    # Create an image object from byte data
    image = Image.open(io.BytesIO(image_bytes))
    # Display the image in the Streamlit app
    st.image(image, caption=caption, use_container_width=True)

# Streamlit app layout
st.title("Chat ")  # App title

# Sidebar for navigation
st.sidebar.title("Options")  # Sidebar title
choice = st.sidebar.radio("Select an Option", ["Image Generation"])  # User option for navigation

# Image generation section
if "generated_image_bytes" not in st.session_state:
    # Initialize session state for generated images
    st.session_state.generated_image_bytes = None

if choice == "Image Generation":
    # Header for the image generation section
    st.header("Image Generation - Stable Diffusion")
    
    # Text area for entering the image description
    user_prompt = st.text_area("Describe the image you want to generate:")

    if st.button("Generate Image"):  # Button to trigger image generation
        if user_prompt.strip():  # Check if the image description is not empty
            # Generate the image based on the description
            generated_image_bytes = query_image_generation(user_prompt)
            if generated_image_bytes:
                # Save the generated image bytes in the session state
                st.session_state.generated_image_bytes = generated_image_bytes
                # Display the generated image
                image = Image.open(io.BytesIO(generated_image_bytes))
                st.image(image, caption="Generated Image", use_container_width=True)
        else:
            # Warning if the description is empty
            st.warning("Please enter a description to generate an image.")

    if st.button("Download Generated Image"):  # Button to download the generated image
        if st.session_state.generated_image_bytes:  # Check if an image has been generated
            # Save the generated image as a PNG file
            image = Image.open(io.BytesIO(st.session_state.generated_image_bytes))
            image.save("generated_image.png")
            st.success("Image saved as generated_image.png")  # Success message
        else:
            # Warning if there is no image to download
            st.warning("No image to save. Please generate an image first.")
