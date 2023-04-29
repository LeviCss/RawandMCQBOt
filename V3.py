# import the modules
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import os
# load .env file
from dotenv import load_dotenv
load_dotenv()

pdf_file = input("Enter the name of the PDF file: ")
reader = PdfReader(pdf_file)

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

text_splitter = CharacterTextSplitter(        
    separator = "\\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

def generate_response(prompt):
    # Find the most relevant parts of the PDF file for the given prompt
    # using the embeddings created from the PDF file
    relevant_text = find_relevant_text(prompt, texts, embeddings)

    # Generate a response based on the relevant text
    response = generate_response_from_text(relevant_text)

    return response

def find_relevant_text(prompt, texts, embeddings):
    # Use embeddings and similarity search to find the most relevant text
    # in the PDF file for the given prompt
    # ...
    return relevant_text

def generate_response_from_text(text):
    # Use text generation techniques to generate a response based on
    # the given text
    # ...
    return response

while True:
    user_input = input("User: ")
    response = generate_response(user_input)
    print(f"Chatbot: {response}")