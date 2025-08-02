
import streamlit as st
import pandas as pd
import plotly.express as px

def create_dashboard(data):
    st.title("Dashboard de Visualización de Datos")

    #Convertir la entrada de datos a DataFrame de pandas.
    df = pd.read_json('data.json')

    #Metricas sugeridas
    metric1 = df['nivelestudios'].value_counts()
    metric2 = df['facultad'].value_counts()

    #Visualización de las metricas usando Plotly Express.
    fig1 = px.bar(x=metric1.index, y=metric1.values, title='Número de estudiantes por nivel de estudios', labels={'x': 'Nivel de estudios', 'y': 'Número de estudiantes'})
    fig2 = px.bar(x=metric2.index, y=metric2.values, title='Número de estudiantes por facultad', labels={'x': 'Facultad', 'y': 'Número de estudiantes'})

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    # Filtrar correos de personas mayores de 40 años
    if int(df['edad'][0]) > 40:
        st.subheader("Correos de personas mayores de 40 años:")
        st.write(df['email'][0])
    else:
        st.subheader("No hay personas mayores de 40 años en el conjunto de datos.")


def app():
    data = {'division': 'ciencias de la salud', 'cau': 'sede bogota', 'codigosnies': '1091', 'edad': '53', 'estadofin': 'admitido', 'email': 'dora.venegas.espinosa@gmail.com', 'genero': 'f', 'facultad': 'fac. de psicologia', 'programa': 'maestria en psicologia clinica y de la familia', 'seccional': 'bogota', 'telefono': '3143949033', 'tipoidentificacion': 'cc', 'numeroidentificacion': '39784176', 'nivelestudios': 'maestria', 'nivelformacion': 'postgrado', 'periodoacademico': '2023-1', 'tipoinscripcion': 'normal'}
    create_dashboard(data)

if __name__ == "__main__":
    app()

