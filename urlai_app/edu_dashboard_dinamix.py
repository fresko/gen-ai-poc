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
    #st.sidebar.title("Navegación")
    with st.sidebar:
        st.title("DataWise")
        st.header("DataWise:")
        st.subheader("Agentes IA")
        st.page_link("edu_dashboard.py", label="Dashboard Principal", icon="📊")
        st.page_link("pages/detailed_analysis.py", label="Conexiones Interpretación", icon="🔌")
        
        # Existing dashboard code
        #...existing code...


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
