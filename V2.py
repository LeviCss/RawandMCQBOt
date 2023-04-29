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

def generate_response(user_input):
    # Use user_input, embeddings, and OpenAI GPT-3/3.5 API to generate a response
    response = "Sorry, I don't know how to answer that yet."
    return response

while True:
    user_input = input("User: ")
    response = generate_response(user_input)
    print(f"Chatbot: {response}")