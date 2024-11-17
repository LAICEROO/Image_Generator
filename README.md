# Image Generation with Stable Diffusion in Streamlit

This project is a **Streamlit web application** that utilizes the **Stable Diffusion** model from Hugging Face to generate images based on user-provided descriptions.

## Features

- Generate images using the Stable Diffusion model.
- Display the generated images directly in the application.
- Download the generated images as `.png` files.

## Requirements

To run this application, you need the following:

- Python 3.8 or later.
- A Hugging Face API key with access to the `stabilityai/stable-diffusion-2` model.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/streamlit-stable-diffusion.git
   cd streamlit-stable-diffusion
   ```
   
2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a .env file in the project directory and add your Hugging Face API key:
```
API_KEY=your_hugging_face_api_key
```

4. Run the Streamlit application:
```
streamlit run app.py
```
## Usage
1. Open the app in your browser (the terminal will display the local URL).
2. Enter a description of the image you want to generate.
3. Click "Generate Image" to create an image.
4. View the generated image in the app.
5. (Optional) Click "Download Generated Image" to save the image as generated_image.png.

## Technologies Used
- Streamlit: For creating the web app.
- Hugging Face API: For accessing the Stable Diffusion model.
- Pillow: For image processing in Python.
