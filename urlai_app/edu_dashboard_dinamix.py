import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Educational Analytics Dashboard", layout="wide")

def load_data(file):
    data = json.load(file)
    df = pd.DataFrame(data)
    # Store dataframe in session state
    st.session_state.df = df
    return df

def create_dashboard(df):
    # Add navigation section at top
    st.sidebar.title("Navegación")
    st.sidebar.page_link("pages/edu_dashboard.py", label="Dashboard Principal")
    st.sidebar.page_link("pages/detailed_analysis.py", label="Análisis Detallado")
    
    # Existing dashboard code
    #...existing code...

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

if __name__ == "__main__":
    main()
