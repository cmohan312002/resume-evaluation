import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
api_key = "AIzaSyDh3OmwHnBCgmjMDhFAV-mVSh9MGGw4h9IS"
genai.configure(api_key=api_key)


# Define the input prompt``
input_prompt = """
You are an experienced (HR) Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Provide improvement suggestions based on job descriptions.
"""

# Function to process all pages of the PDF
def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())  # Convert PDF to images
    pdf_parts = []

    for image in images:
        img_byte_arr = io.BytesIO()  # Convert each page to bytes
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts.append({
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
        })
    
    return pdf_parts

# Function to get Gemini AI response
def get_gemini_response(job_desc, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([job_desc] + pdf_content + [prompt])  # Pass all pages
    return response.text

# Streamlit UI
st.title("SmartCV Analyzer")

# Upload PDF
uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

# Job Description Input
job_description = st.text_area("Enter Job Description", placeholder="e.g., Data Engineer role requiring SQL, Python, and Big Data experience")

if st.button("Evaluate CV"):
    if uploaded_file and job_description:
        try:
            st.info("Processing resume...⏳")
            pdf_content = input_pdf_setup(uploaded_file)  # Convert PDF to images
            response = get_gemini_response(job_description, pdf_content, input_prompt)  # Get AI response

            # Display AI response
            st.success("✅ Evaluation Complete!")
            st.subheader("AI Evaluation Report:")
            st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a PDF and enter a job description.")