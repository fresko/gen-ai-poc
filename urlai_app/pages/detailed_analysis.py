import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Debe estar al principio del script
st.set_page_config(page_title="Laboratorio de Datos", layout="wide")

with st.sidebar:
        st.title("Agente DataWise 👨‍💼💬🤖")
        
        st.subheader("MultiAgentes IA")
        st.page_link("edu_dashboard.py", label="Dashboard Principal", icon="📊")
        st.page_link("pages/detailed_analysis.py", label="Laboratorio de Datos", icon="🧪")

def show_detailed_analysis():
    st.title("Laboratorio de Datos")
    
    st.image("img/laboratoriodedatos3.jpeg", use_container_width=True, caption="Data Lab")
    
    # Inicializar la lista de conexiones en session state
    if "connections" not in st.session_state:
        st.session_state.connections = []
    
    # Lista de emojis para usar como logos
    emojis = ["🚀", "🔍", "🤖", "🌟", "🔒", "💾", "⚡", "🦉", "🐘", "🐧", "🐍", "🌐", "💾", "💻"]

    st.markdown("### Agregar Nueva Conexión 🔌")

    with st.form("form_nueva_conexion", clear_on_submit=True):
        conn_name = st.text_input("Nombre de la Conexión", placeholder="Ej. Mi Base de Datos")
        conn_type = st.selectbox("Tipo de Conexión", options=["MySQL", "Oracle", "Snowflake", "API Rest JSON"])
        conn_string = st.text_input("Cadena de Conexión", placeholder="Cadena de conexión o URL de la API")
        
        submit_form = st.form_submit_button("Agregar Conexión")

    if submit_form:
        # Seleccionar un emoji aleatorio como logo
        random_emoji = random.choice(emojis)
        
        nueva_conexion = {
            "nombre": conn_name,
            "tipo": conn_type,
            "conexion": conn_string,
            "logo": random_emoji,  # Emoji aleatorio
            "estado": "No probado"  # Estado inicial
        }
        st.session_state.connections.append(nueva_conexion)
        st.success(f"Conexión '{conn_name}' agregada con logo {random_emoji}.")

    st.markdown("### Lista de Conexiones")

    if st.session_state.connections:
        for idx, conn in enumerate(st.session_state.connections):
            col1, col2, col3, col4, col5 = st.columns([2,2,4,1,2])
            with col1:
                st.write(f"**{conn['nombre']}**")
            with col2:
                st.write(conn["tipo"])
            with col3:
                st.write(conn["conexion"])
            with col4:
                # Mostrar el emoji como logo
                st.markdown(f"<h1 style='text-align: center; font-size: 2rem;'>{conn['logo']}</h1>", unsafe_allow_html=True)
            with col5:
                if st.button("Interpretar 🤖", key=f"test_{idx}"):
                    # Simulación de prueba
                    conn["estado"] = "Activa"
                    st.success(f"Conexión '{conn['nombre']}'💾 Interpretado con éxito.")
                st.write(f"Estado: {conn['estado']}")
    else:
        st.info("No hay conexiones agregadas aún.")

if __name__ == "__main__":
    show_detailed_analysis()
