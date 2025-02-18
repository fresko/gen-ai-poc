import streamlit as st
import pandas as pd
import json
import plotly.express as px
                        
def app():
    st.title("Hola Mundo - 😎")
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
                              labels={"Cantidad": "Número de Inscripciones"})
            st.plotly_chart(fig_tipo)
        else:
            st.info("No hay datos sobre el tipo de inscripción para visualizar")
                
    except Exception as e:
        st.error("Error al cargar o procesar los datos")
    
if __name__ == "__main__":
    app()
