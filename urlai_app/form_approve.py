import streamlit as st
import os
import json
#from dotenv import load_dotenv


#load_dotenv()

st.set_page_config('preguntaDOC')
#OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
st.header("FORMULARIO DE APROBACIÓN")
st.write("*")

# Cargar el archivo JSON
#json_file_path = 'ruta/al/archivo.json'
json_file = st.file_uploader("Carga tu documento", type="json", on_change=st.cache_resource.clear)

if not json_file:
    st.stop()
#with open(json_file_path, 'r') as file:
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
