import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import google_palm
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            # Extract text from each page and append it to the text variable:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overloop=200)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GooglePalmEmbeddings()
    vector_store = FAISS.from_texts(text_chunks,embeddings=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    llm =google_palm()
    memory =ConversationBufferMemory(memory_key="chat_history",return_message=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=vector_store.as_retriever(),memory=memory)
    return conversation_chain