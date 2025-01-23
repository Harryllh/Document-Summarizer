import os
import openai
from openai import OpenAI
from flask import Flask, render_template, request, flash, redirect, url_for
import PyPDF2

app = Flask(__name__)

# Set up the OpenAI API key using an environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the route for the home page
@app.route('/', methods=['GET'])
def index():
    # Render the main HTML template when a GET request is received
    return render_template('index.html')

# Define the route for handling text summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    # Extract text input from the form submission
    input_text = request.form.get('input_text', '')

    # Handle file upload from the form
    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename != '':
        if uploaded_file.filename.endswith('.pdf'):
            # Use PyPDF2 to extract text from the uploaded PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pdf_text = ""
            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()
            input_text += " " + pdf_text
        else:
            # Flash an error if the uploaded file is not a PDF
            flash("Only PDF files are supported. Please upload a valid PDF file.", "error")
            return redirect(url_for("index"))

    # Retrieve the summary length preference from the form and adjust instructions
    summary_length = request.form.get('summary_length', 'medium')
    if summary_length == 'short':
        length_instruction = "in 1-2 concise sentences"
    elif summary_length == 'long':
        length_instruction = "in multiple paragraphs with detail"
    else:  # Default to 'medium' if no valid input is provided
        length_instruction = "in a short paragraph"

    # Define the prompts for generating both the summary and key points
    summary_prompt = f"""
    You are an assistant that summarizes text. 
    Summarize the following text {length_instruction}.
    Text to summarize:
    {input_text}
    """

    key_points_prompt = f"""
    You are an assistant that summarizes text. 
    Summarize the following text into bullet points.
    Here's the text to summarize:
    {input_text}
    """

    # Initialize the OpenAI client
    client = OpenAI()

    try:
        # Call the OpenAI API to generate the summary
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            store=True,
            messages=[
                {"role": "user", "content": summary_prompt}
            ]
        )
        # Extract the summary text from the API response
        summary = summary_response.choices[0].message.content

        # Call the OpenAI API to generate key points
        key_points_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            store=True,
            messages=[
                {"role": "user", "content": key_points_prompt}
            ]
        )
        # Extract key points and clean up bullet formatting
        key_points = key_points_response.choices[0].message.content
        key_points_list = key_points.split("\n")
        key_points_list = [key_point.strip("-•* ") for key_point in key_points_list if key_point]

        # Render the template with the generated summary and key points
        return render_template('index.html', summary=summary, key_points=key_points_list)

    except Exception as e:
        # Handle any errors from the OpenAI API and notify the user
        print("Error with OpenAI API:", e)
        return render_template('index.html', summary="An error occurred. Please try again.", key_points=[])

# Run the Flask application in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)
