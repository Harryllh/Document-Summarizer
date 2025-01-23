# Flask PDF Summarizer App

This project is a Flask-based web application that allows users to upload PDF files or input text to generate summaries and key points using OpenAI's GPT models.

---

## Prerequisites

1. **Python 3.10**: Ensure Python 3.10 is installed on your system.
2. **Pip**: Python package manager (comes with Python installations).
3. **OpenAI API Key**: Obtain an API key from OpenAI.

---

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/Harryllh/Document-Summarizer.git
cd Document-Summarizer
```

### 2. Create and Activate a Python 3.10 Virtual Environment

```
conda create -n summarizer python=3.10
conda activate summarizer
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Set Up the OpenAI API Key
```
export OPENAI_API_KEY=<your_openai_api_key>
```
Replace <your_openai_api_key> with your actual OpenAI API key.

## Running the Application
### 1. Start the Flask development server
```
python app.py
```
### 2. Once the server is running, you’ll see output like this
```
* Running on http://127.0.0.1:5000
```
Copy the link and paste it into your web browser to access the application.

## Application Features
- Text Input Summarization: Paste text directly into the input box for summarization.
- PDF Summarization: Upload a PDF file to extract and summarize its content.
- Summary Length Options: Choose between short, medium, and long summaries.
- Key Points Extraction: Extract key points in bullet form from the input text or PDF.