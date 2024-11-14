import streamlit as st
import os
import json
import PyPDF2
import tempfile
import time
#from dotenv import load_dotenv


#load_dotenv()

st.set_page_config('Approve')
#OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
st.header("FORMULARIO DE APROBACIÓN")
st.write("*")

# Subir el archivo PDF
pdf_file = st.file_uploader("Carga tu documento PDF", type="pdf")

if pdf_file is not None:
    # Crear un archivo temporal para guardar el PDF
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_file.read())
        temp_file_path = temp_file.name

    # Leer el archivo PDF
    pdf_reader = PyPDF2.PdfReader(temp_file_path)
    num_pages = pdf_reader.numPages

    # Mostrar la barra de progreso
    progress_bar = st.progress(0)
    for i in range(num_pages):
        time.sleep(0.1)  # Simular tiempo de procesamiento
        progress_bar.progress((i + 1) / num_pages)

    # Visualizar el PDF
    st.subheader("Visualizador de PDF")
    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        st.write(page.extract_text())
else:
    st.stop()

# Cargar el archivo JSON
json_file = st.file_uploader("Carga tu documento", type="json", on_change=st.cache_resource.clear)

if not json_file:
    st.stop()

# Leer el archivo JSON
json_data = json.load(json_file)

# Crear dos columnas
col1, col2 = st.columns(2)

# Visualizador del código JSON en la primera columna
with col1:
    st.subheader("Visualizador de JSON")
    st.json(json_data)

# Formulario con los campos del JSON en la segunda columna
with col2:
    st.subheader("Formulario de Aprobación")
    form = st.form(key='approval_form')
    for key, value in json_data.items():
        form.text_input(label=key, value=value)
    submit_button = form.form_submit_button(label='Enviar')
