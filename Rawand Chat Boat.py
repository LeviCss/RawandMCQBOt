{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# import the modules\n",
    "from PyPDF2 import PdfReader\n",
    "from langchain.embeddings.openai import OpenAIEmbeddings\n",
    "from langchain.text_splitter import CharacterTextSplitter\n",
    "from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS\n",
    "import os\n",
    "# load .env file\n",
    "from dotenv import load_dotenv\n",
    "load_dotenv()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "reader = PdfReader('ipc.pdf')"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "raw_text = ''\n",
    "for i, page in enumerate(reader.pages):\n",
    "    text = page.extract_text()\n",
    "    if text:\n",
    "        raw_text += text"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "text_splitter = CharacterTextSplitter(        \n",
    "    separator = \"\\n\",\n",
    "    chunk_size = 1000,\n",
    "    chunk_overlap  = 200,\n",
    "    length_function = len,\n",
    ")\n",
    "texts = text_splitter.split_text(raw_text)"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "len(texts)"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "embeddings = OpenAIEmbeddings()"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle\n",
    "with open(\"foo.pkl\", 'wb') as f:\n",
    "    pickle.dump(embeddings, f)"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(\"foo.pkl\", 'rb') as f:\n",
    "    new_docsearch = pickle.load(f)\n",
    "\n",
    "docsearch = FAISS.from_texts(texts, new_docsearch)"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "query = \"what is the punishment for murder\"\n",
    "docs = docsearch.similarity_search(query)\n",
    "print(docs[0].page_content)"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from langchain.chains.question_answering import load_qa_chain\n",
    "from langchain.llms import OpenAI"
   ]
  },
  {
   "cell_type": "code",
    "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "chain = load_qa_chain(OpenAI(temperature=0), chain_type=\"stuff\")\n",
    "chain.run(input_documents=docs, question=query)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9 (tags/v3.10.9:1dd9be6, Dec  6 2022, 20:01:21) [MSC v.1934 64 bit (AMD64)]"
  },
  "orig_nbformat": 4,
  "vscode": {
   "interpreter": {
    "hash": "3bdefd094ccb8bd3365ae8c21bf36ef46047804461a4c589742842225130b2b8"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}