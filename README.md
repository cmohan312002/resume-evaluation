# SmartCV Analyzer

SmartCV Analyzer is an AI-powered resume evaluation tool that analyzes a candidate's resume against a given job description using Google's Gemini AI. The tool extracts text from the uploaded PDF, processes it, and generates an insightful evaluation report highlighting strengths, weaknesses, and areas for improvement.

## 🚀 Features
- Upload a resume in PDF format 📄
- Input a job description 🏢
- AI-based evaluation using Gemini AI 🤖
- Highlights strengths and weaknesses of the resume 📊
- Suggests improvements for better job alignment 🔍
- Runs within a **Streamlit** web application 🎨

## 🛠️ Tech Stack
- **Python** 🐍
- **Streamlit** for UI
- **pdf2image** for PDF processing
- **PIL (Pillow)** for image handling
- **Google Generative AI (Gemini API)** for evaluation

## 🔧 Installation
### Prerequisites
- Python 3.8+
- Google Generative AI API Key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/cmohan312002/resume-evaluation.git
   cd resume-evaluation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Store your API key securely** in Streamlit secrets:
   ```bash
   mkdir -p ~/.streamlit
   echo "[secrets]" > ~/.streamlit/secrets.toml
   echo "GOOGLE_API_KEY='your-api-key-here'" >> ~/.streamlit/secrets.toml
   ```

## 🏃‍♂️ Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Upload a resume (PDF format).
3. Enter a job description.
4. Click **Evaluate CV** to get AI-generated feedback.

## 📌 Deployment on Streamlit Cloud
1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Deploy the app and add the API key under `Secrets` in the Streamlit settings.

## 🔒 Security Best Practices
- **Never hardcode API keys** in the source code.
- Use **Streamlit secrets** for storing sensitive information.

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 📞 Contact
For any queries or contributions, reach out via email at `cmohan312002@gmail.com` or create an issue in the repository.

Happy coding! 🚀

