import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Generador de Figuras Geométricas", layout="wide")

def generar_figura_random():
    # Limpiar el plot anterior
    plt.clf()
    
    # Lista de figuras posibles
    figuras = ['círculo', 'triángulo', 'cuadrado', 'rectángulo', 'pentágono']
    figura = random.choice(figuras)
    
    # Colores aleatorios
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    
    # Generar figura seleccionada
    if figura == 'círculo':
        circle = plt.Circle((0.5, 0.5), 0.3, color=color)
        plt.gca().add_patch(circle)
        
    elif figura == 'triángulo':
        vertices = np.array([[0.2, 0.2], [0.8, 0.2], [0.5, 0.8]])
        triangle = plt.Polygon(vertices, color=color)
        plt.gca().add_patch(triangle)
        
    elif figura == 'cuadrado':
        square = plt.Rectangle((0.2, 0.2), 0.6, 0.6, color=color)
        plt.gca().add_patch(square)
        
    elif figura == 'rectángulo':
        rectangle = plt.Rectangle((0.2, 0.3), 0.6, 0.4, color=color)
        plt.gca().add_patch(rectangle)
        
    elif figura == 'pentágono':
        angles = np.linspace(0, 2*np.pi, 6)[:-1]
        vertices = np.array([[0.5 + 0.3*np.cos(angle), 0.5 + 0.3*np.sin(angle)] for angle in angles])
        pentagon = plt.Polygon(vertices, color=color)
        plt.gca().add_patch(pentagon)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    return figura, color

def main():
    st.title("🎨 Generador de Figuras Geométricas")
    
    # Columnas para organizar el layout
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.write("### Panel de Control")
        if st.button("🎲 Generar Nueva Figura"):
            figura, color = generar_figura_random()
            st.session_state.figura_actual = figura
            st.session_state.color_actual = color
    
    with col1:
        if st.button("🔄 Generar"):
            figura, color = generar_figura_random()
            st.write(f"### Se generó un {figura}")
            st.pyplot(plt.gcf())
            
            # Información adicional
            st.write(f"**Color:** {color}")
            st.write(f"**Tipo:** {figura}")

if __name__ == "__main__":
    main()