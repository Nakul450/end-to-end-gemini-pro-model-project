from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision model and get response
def get_gemini_response(input, image, prompt):
    try:
        # Loading the Gemini model
        model = genai.GenerativeModel(' gemini-1.5-flash')
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("No file uploaded.")
        raise FileNotFoundError("No file uploaded.")

# Initialize Streamlit app
st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")

# User input
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Input prompt for the Gemini model
input_prompt = """
You are an expert in understanding invoices. You will
receive input images as invoices, and you will have to
answer questions based on the input image.
"""

# Submit button
if st.button("Tell me about the invoice"):
    try:
        # Process uploaded image
        image_data = input_image_setup(uploaded_file)

        # Get response from Gemini model
        response = get_gemini_response(input_prompt, image_data, input_text)

        # Display response
        st.subheader("The response is:")
        if response:
            try:
                # If response is JSON, parse it
                st.json(response)
            except ValueError:
                # Fallback if response is not JSON
                st.write("Response:", response)
        else:
            st.error("No response received from the Gemini model.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")







