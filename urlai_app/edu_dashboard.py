import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import random
import importlib.util
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(page_title="Educational Analytics Dashboard", layout="wide")

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

    ##Config Gemini AI
def crete_prompt(selected_llm,prompt):
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
        )
        #files = genai.upload_file(file_content, mime_type="application/pdf")
       # print(f"Uploaded file '{files.display_name}' as: {files.uri}")
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        #files,
                        prompt,
                    ],
                },
            ]
        )
        response = chat_session.send_message("INSERT_INPUT_HERE")
        return response

def main():
    st.title("Dashboard de Análisis Educativo")
    
    uploaded_file = st.file_uploader("Cargar archivo JSON", type=['json'])
    
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            create_dashboard(df)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
    else:
        st.info("Por favor carga un archivo JSON para visualizar el dashboard")

    #########
    # Additional code for generating dynamic pages
    #########
    # # Initialize session state for page counter and generated pages list
    if uploaded_file is not None:
        
#       OPENAI_API_KEY = st.text_input('OpenAI API Key', type='password')
        st.header("AGENTE AI - PREGUNTA A TU PDF")
        GOOGLE_API_KEY = st.text_input('GOOGLE_API_KEY', type='password')
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

         # Crear una lista de tres valores
        options = ["gemini-1.5-flash-002", "gemini-1.0-pro", "gemini-1.5-pro","gemini-2.0-flash-exp","gemini-2.0-pro-exp"]
        
        # Crear un selectbox en Streamlit
        selected_llm = st.selectbox("Selecciona el modelo LLM:", options)
        
        # Mostrar el valor del ítem seleccionado
        st.write(f"Has seleccionado: {selected_llm}")

        prompt = st.text_input("Escribe tu nombre")
        # Input for name and button to generate a new page
        btn_agente = st.button("Crea tu dashboard")
        if btn_agente:
            st.write("Generando Dashboard...")
            response_llm = crete_prompt(selected_llm,prompt)
            st.write(response_llm.text)

            #st.write

            if "page_counter" not in st.session_state:
                st.session_state.page_counter = 1
            if "generated_pages" not in st.session_state:
                st.session_state.generated_pages = []

        
        
                # List of random emoticons
                emoticons = ["😀", "😎", "🥳", "🤖", "😂"]
                random_emoticon = random.choice(emoticons)
                
                # Create new page filename using the counter
                page_filename = f"page_{st.session_state.page_counter}.py"
                with open(page_filename, "w", encoding="utf-8") as f:
                    f.write(f'''import streamlit as st
import pandas as pd
import json
import plotly.express as px
                        
def app():
    st.title("Hola Mundo - {random_emoticon}")
    st.write("Codigo Generado, !")
    st.title("Dashboard de Administración Educativa")   
    
    try:
        df = pd.read_json("data.json")
        # Convertir columna "edad" a numérico si existe
        if "edad" in df.columns:
            df["edad"] = pd.to_numeric(df["edad"], errors="coerce")
            
        # Métricas clave:
        # 1. Total de estudiantes
        # 2. Total de estudiantes admitidos (estadofin == "admitido")
        col1, col2 = st.columns(2)
        with col1:
            total_estudiantes = len(df)
            st.metric("Total de Estudiantes", total_estudiantes)
        with col2:
            if "estadofin" in df.columns:
                total_admitidos = len(df[df["estadofin"].str.lower() == "admitido"])
                st.metric("Total de Estudiantes Admitidos", total_admitidos)
            else:
                st.metric("Total de Estudiantes Admitidos", "N/A")
                
        # Dashboard de visualización de distribución sugerido para datos académicos
        # Tercera gráfica: Distribución de Tipo de Inscripción
        if "tipoinscripcion" in df.columns:
            tipo_counts = df["tipoinscripcion"].value_counts().reset_index()
            tipo_counts.columns = ["Tipo de Inscripción", "Cantidad"]
            fig_tipo = px.bar(tipo_counts, x="Tipo de Inscripción", y="Cantidad", 
                              title="Distribución de Tipo de Inscripción",
                              labels={{"Cantidad": "Número de Inscripciones"}})
            st.plotly_chart(fig_tipo)
        else:
            st.info("No hay datos sobre el tipo de inscripción para visualizar")
                
    except Exception as e:
        st.error("Error al cargar o procesar los datos")
    
if __name__ == "__main__":
    app()
''')
                # Append the new page file to the list & update counter
                st.session_state.generated_pages.append(page_filename)
                st.session_state.page_counter += 1
                st.success(f"Página generada: {page_filename}")
                
                # Load and execute the generated page inline
                spec = importlib.util.spec_from_file_location("generated_page", page_filename)
                generated_page = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(generated_page)
                if hasattr(generated_page, "app"):
                    st.markdown("### Contenido de la página generada")
                    generated_page.app()
                

if __name__ == "__main__":
    main()
