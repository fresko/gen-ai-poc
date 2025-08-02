import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import random
import importlib.util
import google.generativeai as genai
import tempfile
from tempfile import NamedTemporaryFile
import ast
from dotenv import load_dotenv

#st.set_page_config(page_title="Educational Analytics Dashboard", layout="wide")

with st.sidebar:
        st.title("Agente DataWise 👨‍💼💬🤖")
        
        st.subheader("MultiAgentes IA")
        st.page_link("edu_dashboard.py", label="Dashboard Principal", icon="📊")
        st.page_link("pages/detailed_analysis.py", label="Laboratorio de Datos", icon="🧪")

def load_data(file):
    data = json.load(file)
    df = pd.DataFrame(data)
    return df

def create_dashboard(df):
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(df)
        st.metric("Total Estudiantes", total_students)
        
    with col2:
        if 'edad' in df.columns:
            df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
            avg_age = round(df['edad'].mean(), 1)
            st.metric("Edad Promedio", avg_age)
        else:
            st.metric("Edad Promedio", "N/A")
        
    with col3:
        postgrado_count = len(df[df['nivelformacion'] == 'postgrado'])
        st.metric("Total Postgrado", postgrado_count)
        
    with col4:
        pregrado_count = len(df[df['nivelformacion'] == 'pregrado'])
        st.metric("Total Pregrado", pregrado_count)

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Estado de admisión
        estado_counts = df['estadofin'].value_counts()
        fig_estado = px.pie(values=estado_counts.values, 
                          names=estado_counts.index,
                          title='Distribución por Estado de Admisión')
        st.plotly_chart(fig_estado)

    with col2:
        # Tipo de inscripción
        tipo_counts = df['tipoinscripcion'].value_counts()
        fig_tipo = px.bar(x=tipo_counts.index, 
                         y=tipo_counts.values,
                         title='Distribución por Tipo de Inscripción')
        st.plotly_chart(fig_tipo)

    # Age distribution
    fig_age = px.histogram(df, 
                          x='edad',
                          title='Distribución de Edades',
                          nbins=20)
    st.plotly_chart(fig_age)

    # Program level distribution by faculty
    prog_faculty = pd.crosstab(df['facultad'], df['nivelformacion'])
    fig_prog = px.bar(prog_faculty,
                      title='Nivel de Formación por Facultad',
                      barmode='group')
    st.plotly_chart(fig_prog)

def extract_strucutre(file):
    #data = json.load(file)
        data = {
        "division": "ciencias de la salud",
        "cau": "sede bogota",
        "codigosnies": "1091",
        "edad": "53",
        "estadofin": "admitido",
        "email": "dora.venegas.espinosa@gmail.com",
        "genero": "f",
        "facultad": "fac. de psicologia",
        "programa": "maestria en psicologia clinica y de la familia",
        "seccional": "bogota",
        "telefono": "3143949033",
        "tipoidentificacion": "cc",
        "numeroidentificacion": "39784176",
        "nivelestudios": "maestria",
        "nivelformacion": "postgrado",
        "periodoacademico": "2023-1",
        "tipoinscripcion": "normal"
        }
        #df = pd.DataFrame(data)
        return data

    ##Config Gemini AI
def crete_prompt(structure_data,selected_llm,prompt):
        #prompt = "identifica los grupos de informacion o entidades de negocio y regeresalo en formato json simple clave valor con los datos  contenidos en el archivo adjunto"
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            #model_name="gemini-1.5-flash-002",       
            model_name=selected_llm,       
            generation_config=generation_config,
            system_instruction="eres un desarrollador experto en py y streamlit y visualizacion de datos, según  esta estructura de datos json exactamente igual sin cambiar su nombres de campos , entiende la estructra  y genera  visulizaciones clave best fit  para crear un interactivo  dashboard  en el ambito de la educacion o para rectores y administrativos de la universidad  ,genera codigo py para dashboard de visualizacion dinámico , según  la estructura  de datos entregada ,  en la respuesta solo codigo en py y streamlit , los gráficos con librería plotly.express  ,ten encuenta este codigo es para una  sola pagina , incluye el bloque de ejecucion  main que llame la funcion app . sin explicaciones.",
        )
        #files = genai.upload_file(filedata, mime_type="text/plain")
        #print(f"Uploaded file '{files.display_name}' as: {files.uri}")
        print("Estructura de datos : ",structure_data)
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        #files,
                        "estructura de datos : "+str(structure_data)+ " "+prompt,
                    ],
                },
            ]
        )
        response = chat_session.send_message("INSERT_INPUT_HERE")
        return response

def main():
    st.title("Análisis de Datos - BI Aumentada con IA")
    
    uploaded_file = st.file_uploader("Cargar Datos Interpretado por Agente de Datos", type=['json'])
    
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            create_dashboard(df)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
    else:
        st.info("Selecciona archivo de Datos Interpretado por Agente de Datos para visualizar el dashboard")

    #########
    # Additional code for generating dynamic pages
    #########
    # # Initialize session state for page counter and generated pages list
    if uploaded_file is not None:
        
#       OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
        st.header("AGENTE AI - PREGUNTALE A TUS DATOS 👨‍💼💬🤖")
        GOOGLE_API_KEY = st.text_input('GOOGLE_API_KEY', type='password')
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

         # Crear una lista de tres valores
        options = ["gemini-1.5-flash-002", "gemini-1.0-pro", "gemini-1.5-pro","gemini-2.0-flash-exp","gemini-2.0-pro-exp"]
        
        # Crear un selectbox en Streamlit
        selected_llm = st.selectbox("Selecciona el modelo LLM:", options)
        
        # Mostrar el valor del ítem seleccionado
        st.write(f"Has seleccionado: {selected_llm}")

        #ruta de file upload
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_path = tmp_file.name

        # Reemplazar el input de texto por un text_area para tener más espacio
        prompt = st.text_area("Preguntale a DataWise sobre tus datos 🤓", height=150)
        
        # Input for name and button to generate a new page
        #solucion varias veces 
        btn_agente = st.button("Crea tu dashboard")
        if btn_agente:
              
            # Reiniciar las variables de session para forzar una "nueva sesión"
            st.session_state.page_counter = 1
            st.session_state.generated_pages = []
            st.session_state.page_generated = False
            #st.write
            st.write("Generando Dashboard Dinamico...")

            sdata = extract_strucutre(file_path)
            response_llm = crete_prompt(sdata,selected_llm,prompt)
            code_generated = response_llm.text

            #validar

           #try:
                #ast.parse(code_generated)
           
            #st.write(code_generated)
            code_generated_visual = code_generated
            code_generated = code_generated.replace("```python", "")
            code_generated = code_generated.replace("```", "")       
        
                # Supongamos que este código se ejecuta al pulsar un botón (o en cierto evento)
            if not st.session_state.page_generated:
                    # Aquí se incluye el código para generar la página dinámica
                    page_filename = f"page_{st.session_state.page_counter}.py"
                    with open(page_filename, "w", encoding="utf-8") as f:
                        # 'code_generated' es la cadena que contiene el código Python que queremos escribir,
                        # asegurarse de que no contenga marcas Markdown como ```python
                        code_generated = code_generated.replace("df = pd.DataFrame([data])", "df = pd.read_json('data.json')")
                        f.write(f'''{code_generated}''')
                    
                    # Actualizar el estado de sesión
                    st.session_state.generated_pages.append(page_filename)
                    st.session_state.page_counter += 1
                    st.session_state.page_generated = True
                    st.success(f"Página generada: {page_filename}")
                    
                    # Cargar y ejecutar la página generada de forma inline
                    spec = importlib.util.spec_from_file_location("generated_page", page_filename)
                    generated_page = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(generated_page)
                    if hasattr(generated_page, "app"):
                        st.markdown("### Contenido de la página generada")
                        generated_page.app()

            
            with st.expander("Ver código generado", expanded=False):
                st.code(code_generated_visual, language="python")

           # except SyntaxError as e:
                #st.error(f"El código generado contiene errores de sintaxis: {e}")
            #return  # O maneja la situación de error
                

if __name__ == "__main__":
    main()
