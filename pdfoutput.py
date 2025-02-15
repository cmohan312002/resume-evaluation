import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
import sys
import io

# 💡 Configure Gemini API Key (Hardcoded for now, replace with your key)
GENAI_API_KEY = "AIzaSyDh3OmwHnBCgmjMDhFAV-mVSh9MGGw4h9I"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

# 💡 Define AI Prompt
AI_PROMPT = """
You are an expert Python programmer. Given a coding problem from a PDF, generate the correct Python code to solve it.
Ensure that your solution is complete, free from syntax errors, and ready to execute.
"""

# 📜 Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")  # Open PDF file
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page
    return text.strip()

# 🤖 Function to Get AI-Generated Code
def get_gemini_response(problem_statement):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([AI_PROMPT, problem_statement])  # Generate AI response
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# 🚀 Function to Execute Generated Python Code
def execute_python_code(code):
    try:
        # Redirect stdout to capture printed output
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        exec(code, {})  # Execute AI-generated code

        sys.stdout = sys.__stdout__  # Restore standard output
        return output_buffer.getvalue()  # Return captured output
    except Exception as e:
        sys.stdout = sys.__stdout__  # Restore standard output in case of error
        return f"Execution Error: {e}"

# 🎨 Streamlit UI
st.title("📄 AI-Powered Python Problem Solver")

# 🚀 Upload PDF File
uploaded_file = st.file_uploader("Upload a PDF containing Python problems", type=["pdf"])

if uploaded_file:
    st.info("📜 Extracting questions from PDF...")
    extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text:
        st.subheader("📜 Extracted Problem:")
        st.write(extracted_text)

        if st.button("🤖 Generate and Execute Solution"):
            st.info("Generating solution... 🚀")
            generated_code = get_gemini_response(extracted_text)  # Get AI solution

            if generated_code:
                st.subheader("🤖 AI-Generated Python Code:")
                st.code(generated_code, language="python")

                st.info("🔍 Running the code...")
                execution_output = execute_python_code(generated_code)

                st.subheader("🔍 Execution Output:")
                st.write(execution_output)
            else:
                st.error("AI did not generate a valid response. Try again.")
    else:
        st.warning("Could not extract text. Ensure the PDF contains readable text.")

