import streamlit as st
import os

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.embeddings import HuggingFaceEmbeddings 
#from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv
import time




load_dotenv()

st.set_page_config('preguntaDOC')

with st.sidebar:
    with st.sidebar:
    st.header("GEMINI GOOGLE")
    st.image("https://1000marcas.net/wp-content/uploads/2024/02/Gemini-Logo.jpg", width=100)
    with st.sidebar:
    st.header("OPENAI- ChatGPT")
    st.image("https://www.androidheadlines.com/wp-content/uploads/2023/03/GPT-4-logo-1420x799.webp",  width=100)

c.write("This will show second")
#OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
st.header("AGENTE AI - PREGUNTA A TU PDF")
GOOGLE_API_KEY = st.text_input('GOOGLE_API_KEY', type='password')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


       

pdf_obj = st.file_uploader("Carga tu documento", type="pdf", on_change=st.cache_resource.clear)

@st.cache_resource 
def create_embeddings(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
        )        
    chunks = text_splitter.split_text(text)

    #embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    
    
    return knowledge_base


if pdf_obj:
    knowledge_base = create_embeddings(pdf_obj)
    user_question = st.text_input("Haz una pregunta sobre tu PDF:")

    if user_question:
        #os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        #os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        #genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
       

        docs = knowledge_base.similarity_search(user_question, 3)
        #llm = ChatOpenAI(model_name='gpt-4o') #gpt-4o
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.3)
        chain = load_qa_chain(llm, chain_type="stuff")
        respuesta = chain.run(input_documents=docs, question=user_question)

        st.write(respuesta)    