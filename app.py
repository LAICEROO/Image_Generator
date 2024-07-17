from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter
from customtkinter import CTkImage
import ollama
import requests
import io

API_URL = "https://api-inference.huggingface.co/models/Kvikontent/midjourney-v6"
headers = {"Authorization": "Bearer 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"}

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Image Recognition and Generation")
root.geometry('1200x720')

selected_image = None
generated_image_bytes = None

def get_user_text(widget):
    return widget.get("1.0", END).strip()

def request_image_description(entered_text, image_path):
    if not image_path:
        return "No image selected."
    else:
        res = ollama.chat(
            model='llava:13b',
            messages=[
                {'role': 'user',
                 'content': entered_text,
                 'images': [image_path]
                 }
            ]
        )
        return res['message']['content']

def button_click_image_recognition():
    entered_text = get_user_text(user_text)
    response_text = request_image_description(entered_text, selected_image)
    user_text.insert(END, f"\nResponse: {response_text}")

def button_click_image_generation():
    entered_text2 = get_user_text(user_text2)
    global generated_image_bytes
    generated_image_bytes = query_image_generation({"inputs": entered_text2})
    if generated_image_bytes:
        display_generated_image_from_bytes(generated_image_bytes)
    else:
        user_text2.insert(END, "\nNo image bytes received.")

def open_file():
    global selected_image
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        selected_image = file_path
        display_image(file_path)

def display_image(file_path):
    img = Image.open(file_path)
    img = img.resize((1100, 600), Image.LANCZOS)
    img_ctk = ImageTk.PhotoImage(img)
    if hasattr(display_image, 'label'):
        display_image.label.destroy()
    display_image.label = customtkinter.CTkLabel(tab1, image=img_ctk)
    display_image.label.image = img_ctk
    display_image.label.pack(pady=20)

def display_generated_image_from_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((1100, 600), Image.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)

    if hasattr(display_generated_image_from_bytes, 'canvas'):
        display_generated_image_from_bytes.canvas.destroy()

    display_generated_image_from_bytes.canvas = Canvas(tab2, width=1100, height=600)
    display_generated_image_from_bytes.canvas.pack(pady=20)
    display_generated_image_from_bytes.canvas.create_image(0, 0, anchor='nw', image=image_tk)
    display_generated_image_from_bytes.canvas.image = image_tk

def query_image_generation(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print("Error:", response.status_code)
        print("Response:", response.text)
        return None

def download_image():
    global generated_image_bytes
    if generated_image_bytes:
        image = Image.open(io.BytesIO(generated_image_bytes))
        image.save("generated_image.png")
        print("Image saved as generated_image.png")
    else:
        print("No image to save.")

# Create the tabs with specified width and height
tabs = customtkinter.CTkTabview(root, width=1200, height=720)
tabs.pack(pady=20)

# Add tabs to the CTkTabview
tab1 = tabs.add("Image Recognition")
tab2 = tabs.add("Image Generator")

user_text = customtkinter.CTkTextbox(tab1, width=1000, height=120)
user_text.pack(side=BOTTOM, pady=20)

user_text2 = customtkinter.CTkTextbox(tab2, width=1000, height=120)
user_text2.pack(side=BOTTOM, pady=20)

# Create a frame to hold the buttons
button_frame1 = customtkinter.CTkFrame(tab1)
button_frame1.pack(side=BOTTOM, pady=10)

# Create and pack buttons inside the frame for Image Recognition tab
file_button = customtkinter.CTkButton(button_frame1, text="Open File", command=open_file)
file_button.pack(side=LEFT, padx=10)

button_recognition = customtkinter.CTkButton(button_frame1, text="Send", command=button_click_image_recognition)
button_recognition.pack(side=RIGHT, padx=10)

# Create a frame to hold the buttons for the Image Generator tab
button_frame2 = customtkinter.CTkFrame(tab2)
button_frame2.pack(side=BOTTOM, pady=10)

button_generation = customtkinter.CTkButton(button_frame2, text="Send", command=button_click_image_generation)
button_generation.pack(side=LEFT, padx=10)

button_download = customtkinter.CTkButton(button_frame2, text="Download", command=download_image)
button_download.pack(side=RIGHT, padx=10)

root.mainloop()