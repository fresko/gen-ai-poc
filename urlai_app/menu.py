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
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

st.set_page_config('AI AGENT ')
# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1
pdf_obj = None
#Funciones_________________________________
def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            pdf_obj = st.file_uploader("Carga tu documento", type="pdf", on_change=st.cache_resource.clear)
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Start", "AI-Agent", "Contact"],  # required
                icons=["rocket", "robot", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Start", "AI-Agent", "Contact"],  # required
            icons=["rocket", "robot", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )        
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Start", "AI-Agent", "Contact"],  # required
            icons=["rocket", "robot", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected

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


selected = streamlit_menu(example=EXAMPLE_NO)


if selected == "Start":
    st.title(f"Hello Space People ! {selected}")
if selected == "AI-Agent":
    st.title(f"{selected} - Proof of Concept  ")
    tab1, tab2, tab3 = st.tabs(["Google - Gemini", "OpenAI - ChatGPT", "Conversational Data Business "])
    with tab1: #GEMINI
        st.header("Google - Gemini")
        st.image("https://1000marcas.net/wp-content/uploads/2024/02/Gemini-Logo.jpg", width=100)
        load_dotenv()
        st.header("AGENTE AI - PREGUNTA A TU PDF")
        GOOGLE_API_KEY = st.text_input('GOOGLE_API_KEY', type='password')
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        #pdf_obj = st.file_uploader("Carga tu documento", type="pdf", on_change=st.cache_resource.clear)

        if GOOGLE_API_KEY:
            knowledge_base = create_embeddings(pdf_obj)
            user_question = st.text_input("Haz una pregunta sobre tu PDF:")

            if user_question:
                docs = knowledge_base.similarity_search(user_question, 3)
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.3)
                chain = load_qa_chain(llm, chain_type="stuff")
                respuesta = chain.run(input_documents=docs, question=user_question)

                st.write(respuesta)    

    with tab2:
        st.header("OpenAI - ChatGPT")
        st.image("https://www.androidheadlines.com/wp-content/uploads/2023/03/GPT-4-logo-1420x799.webp",  width=100)
        OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        #pdf_obj2 = st.file_uploader("Carga tu documento", type="pdf", on_change=st.cache_resource.clear)
        if OPENAI_API_KEY:
            knowledge_base2 = create_embeddings(pdf_obj))
            user_question2 = st.text_input("Haz una pregunta sobre tu PDF:")

            if user_question2:               
                docs = knowledge_base2.similarity_search(user_question2, 3)
                llm = ChatOpenAI(model_name='gpt-4o') #gpt-4o
                chain = load_qa_chain(llm, chain_type="stuff")
                respuesta2 = chain.run(input_documents=docs, question=user_question)

                st.write(respuesta2)    

    with tab3:
        st.header("Conversational Data Business ")
        st.image("https://www.researchgate.net/profile/Marianna-Charitonidou/publication/360719662/figure/fig1/AS:1157512099299329@1652983798438/DATA-TUNNEL-2020-21-Custom-software-site-specific-installation-Duration-9-minutes.jpg", width=100)
if selected == "Contact":
    st.title(f"You have selected {selected}")