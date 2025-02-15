import streamlit as st
# gradio
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import fitz  # PyMuPDF
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import tempfile


# Define the function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    doc = fitz.open(temp_file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    
    return text

# Define the prompt template
template = """
Provide a score from 1 to 10 and a short reason for your score.
You are an experienced (HR) Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

        I need a comprehensive analysis of the following job description and resume. 
        Provide the report in the following format:

        1. *Overall Match Percentage*:
        - Provide a percentage value indicating how well the resume matches the job description.
        - Example: “Your resume matches 80% of the job requirements.”

        2. *Detailed Skill Match*:
        - List the skills from the job description that match the resume.
        - Highlight the missing skills explicitly.
        - Example:
            - Matched Skills: JavaScript, React, Node.js.
            - Missing Skills: GraphQL, Docker.

        3. *Experience Insights*:
        - Indicate whether the candidate's experience aligns with the job description.
        - Example: “You meet the required 3 years of experience in software development.”

        4. *Improvement Tips*:
        - Suggest actionable steps to improve the resume for better alignment with the job description.
        - Examples:
            - “Add the keyword ‘GraphQL’ to align with the job description.”
            - “Consider detailing your experience with Docker in a project or job role.”
        - Include examples or templates for improvement if applicable
        
Provide improvement suggestions based on job descriptions.
Job Description: {job_description}
Resume: {resume}

"""

prompt = PromptTemplate(input_variables=["job_description", "resume"], template=template)

google_api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.0,
    google_api_key=google_api_key
)

# Create the chain using RunnablePassthrough and RunnableSequence
chain = (
    {"job_description": RunnablePassthrough(), "resume": RunnablePassthrough()}
    | prompt
    | llm
)

# Function to evaluate resume using the new chain
def evaluate_resume(job_description, resume):
    result = chain.invoke({"job_description": job_description, "resume": resume})
    return result

#Frontend
# Streamlit UI
st.title("Resume Evaluation System")

st.header("Input Job Description & Resume")

# Upload resume file
resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Job Description", height=200)

if resume_file and job_description:
    # Extract resume text from PDF
    
    resume_text = extract_text_from_pdf(resume_file)
    
    st.write("Evaluating the resume against the job description...")

    # Evaluate resume
    evaluation = evaluate_resume(job_description, resume_text)

    # Display result
    st.subheader("Evaluation Result")
    st.write(evaluation.content)
else:
    st.write("Please upload a resume and provide a job description to get started.")
