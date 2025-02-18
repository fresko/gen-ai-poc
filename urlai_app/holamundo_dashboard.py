import streamlit as st
import plotly.express as px
import os
import random
import importlib.util

st.set_page_config(page_title="Holamundo Dashboard", layout="wide")

# Initialize session state for page counter and generated pages list
if "page_counter" not in st.session_state:
    st.session_state.page_counter = 1
if "generated_pages" not in st.session_state:
    st.session_state.generated_pages = []

# Pie chart data with 4 data points
data = {
    'Categoria': ['A', 'B', 'C', 'D'],
    'Valor': [10, 20, 30, 40]
}
fig = px.pie(data, names='Categoria', values='Valor', title='Diagrama de Torta')
st.plotly_chart(fig)

# Input for name and button to generate a new page
name = st.text_input("Escribe tu nombre")
if st.button("Generar Página"):
    # List of random emoticons
    emoticons = ["😀", "😎", "🥳", "🤖", "😂"]
    random_emoticon = random.choice(emoticons)
    
    # Create new page filename using the counter
    page_filename = f"page_{st.session_state.page_counter}.py"
    with open(page_filename, "w", encoding="utf-8") as f:
        f.write(f'''import streamlit as st

def app():
    st.title("Hola Mundo - {name} {random_emoticon}")
    st.write("Bienvenido, {name}!")

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

# Display the list of generated pages
st.subheader("Lista de Páginas Generadas")
for page in st.session_state.generated_pages:
    st.write(page)