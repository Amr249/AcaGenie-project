import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv # to import the API keys 
from PyPDF2 import PdfReader 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from HtmlTemplates import user_template, bot_template, css
from langchain.llms import huggingface_hub
from gtts import gTTS
import time







# function to extract text from PDFs
def get_pdf_text(user_pdfs):
    text = "" # variable to store all the text from all the PDFs

    for pdf in user_pdfs: # loop through all the PDFs the user entered
        pdf_reader = PdfReader(pdf) # create a PDF object that have pages 
        for page in pdf_reader.pages: # loop throough the pages 
            text += page.extract_text() # append all the text in each page to text variable 
    return text 


# function to turn the entire extracted text into chunks 
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", # set the seperator as a single line 
        chunk_size=1000, # chunck after a 1000 character 
        chunk_overlap=200,
        length_function=len)
    
    # split all the text into chunks and store it in chunks variable
    chunks = text_splitter.split_text(text)
    return chunks


# function to convert the text chunks into vectors 
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()

    # embeddings = HuggingFaceInstructEmbeddings(model_name ="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = huggingface_hub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})


    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return conversation_chain

# Convert the text dialogue into speech
#def text_to_speech(conversation_chain, output_path):
    #time.sleep(10)
    #tts = gTTS(text=conversation_chain, lang='en')
    #tts.save(output_path)



def handle_user_question(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)



def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    

    # check if conversation is in the session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    


    st.header("Chat with multiple PDFs :books:")

    user_pdfs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    
    if st.button("Process"):
            with st.spinner("Process"):
                # get the PDF text 
                PDF_raw_text = get_pdf_text(user_pdfs)

                # get the text Chunks
                text_chunks = get_text_chunks(PDF_raw_text)
                st.write(text_chunks)

                # create vectore store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain 
                st.session_state.conversation = get_conversation_chain(vectorstore)
    user_question = st.text_input("Ask a question about your documents:")
    
    if user_question:
        handle_user_question(user_question)

    
    

        # assign the PDFs the user entered to user_pdfs variable 
    


if __name__ == '__main__':
    main()