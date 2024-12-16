import openai
import streamlit as st
from tempfile import NamedTemporaryFile
from gtts import gTTS
import pdfplumber
import os
from dotenv import load_dotenv, find_dotenv
import time
from PIL import Image
from io import BytesIO
import requests
import replicate
import time

# Load environment variables from the .env file
load_dotenv(find_dotenv())


# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extracting the text from a PDF file
def extract_text_from_pdf(uploaded_file):
    # Use BytesIO to treat the uploaded file as a file-like object
    pdf_content = BytesIO(uploaded_file.read())  # Reading file bytes into memory
    with pdfplumber.open(pdf_content) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to generate AI-based dialogue using GPT-3 or GPT-4
#def generate_dialogue(papers_text):
    prompt = f"""
    Create a dialogue between three people discussing the following paper:
    
    Paper : {papers_text[0]}

    The participants should include:
    - A host who introduces the papers and facilitates the conversation.
    - A learner who asks questions about the papers and explores key points.
    - An expert who explains the papers in detail and provides insights.

    The dialogue should include multiple exchanges between the host, learner, and expert, creating a dynamic discussion.
    """

    # Generate the dialogue using GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if available, or "gpt-3.5-turbo"
        messages=[ 
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the generated dialogue from the response
    dialogue = response['choices'][0]['message']['content']
    return dialogue

# Convert the text dialogue into speech
def text_to_speech(text, output_path):
    time.sleep(10)
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)

# Function to generate cover art based on the podcast's topic
def generate_cover_art(cover_art_title):
    # Use DALL·E to generate an image based on the podcast title or description
    prompt = f""" Create an artistic podcast cover for a podcast titled '{cover_art_title}'.
            It should reflect the topics discussed in the research paper,
            include things realted to podcasts in the image like Microphone, speaker, Headphones and studio please,
            NOTE that you dont have to include them all just include what is better for the design, ALSO Include no
            Text in the cover image"""

    # Generate the image using OpenAI's DALL·E model
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"  # You can adjust the image size
    )
    
    # Get the URL of the generated image
    image_url = response['data'][0]['url']
    
    # Fetch and load the image
    image = Image.open(BytesIO(requests.get(image_url).content))
    return image


def show_dialoge(papers_text):
    prompt = f"""
    Create a dialogue between three people discussing the following paper:

    Paper : {papers_text[0]}

    The participants should include:
    - A host who introduces the papers and facilitates the conversation.
    - A learner who asks questions about the papers and explores key points.
    - An expert who explains the papers in detail and provides insights.

    The dialogue should include multiple exchanges between the host, learner, and expert, creating a dynamic discussion.
    """

    # Generate the dialogue using GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if available, or "gpt-3.5-turbo"
        messages=[ 
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the generated dialogue from the response
    Podcast_dialogue = response['choices'][0]['message']['content']
    return st.write(Podcast_dialogue)




st.title("Paper to Podcast Web App :studio_microphone: ")


# File upload: Allow user to upload multiple PDF files
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
if uploaded_files:
    papers_text = []

    # Extract text from each uploaded PDF
    for uploaded_file in uploaded_files:
        text = extract_text_from_pdf(uploaded_file)  # Pass the uploaded file directly
        papers_text.append(text)  # Collect the extracted text from all papers

    cover_art_title = st.text_input("Enter the paper title please ")  # You can change this dynamically

    # Ensure that there is at least one paper uploaded for the dialogue generation
    if len(papers_text) >= 1 and cover_art_title is not None:
        #Generate dialogue from the extracted text using GPT
        #dialogue_script = generate_dialogue(papers_text)

        # Generate cover art for the podcast based on the dialogue
        cover_art_image = generate_cover_art(cover_art_title)

        # Display success message
        st.success("Podcast and Cover Art generated successfully!")

        # Display the generated cover art
        st.image(cover_art_image, caption="Podcast Cover Art", use_column_width=True)

        st.success("Podcast script!")
        st.write(papers_text)
        #show_dialoge(papers_text)

        # Convert the dialogue script into speech
        output_audio_path = "generated_podcast.mp3"
        if papers_text:
            combined_text = "\n".join(papers_text)  # Join the list of text into one string
            text_to_speech(combined_text, output_audio_path)

        

        # Provide download link for the generated podcast
        with open(output_audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format='audio/mp3')
            st.download_button("Download Podcast", audio_file, file_name=output_audio_path)
  
    else:
        st.warning("Please upload at least one paper for generating a podcast.")
