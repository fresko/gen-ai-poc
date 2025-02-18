import streamlit as st
import pandas as pd
import plotly.express as px

def show_detailed_analysis():
    st.title("Análisis Detallado")
    
    if 'df' in st.session_state:
        df = st.session_state.df
        
        # Detailed metrics
        st.subheader("Métricas Detalladas")
        
        # Additional visualizations
        inscripcion_faculty = pd.crosstab(df['facultad'], df['tipoinscripcion'])
        fig = px.bar(inscripcion_faculty, 
                     title='Tipos de Inscripción por Facultad',
                     barmode='group')
        st.plotly_chart(fig)
        
    else:
        st.warning("Por favor cargue datos en la página principal primero")

if __name__ == "__main__":
    show_detailed_analysis()