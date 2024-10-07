import streamlit as st
from streamlit_option_menu import option_menu

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1


def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Start", "AI-Agent", "Contact"],  # required
                icons=["rocket", "robot", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Start", "AI-Agent", "Contact"],  # required
            icons=["rocket", "robot", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Start", "AI-Agent", "Contact"],  # required
            icons=["rocket", "robot", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected


selected = streamlit_menu(example=EXAMPLE_NO)


if selected == "Start":
    st.title(f"Hello Space People ! {selected}")
if selected == "AI-Agent":
    st.title(f"{selected} - Proof of Concept  ")
    tab1, tab2, tab3 = st.tabs(["Google - Gemini", "OpenAI - ChatGPT", "Conversational Data Business "])
    with tab1:
        st.header("Google - Gemini")
        st.image("https://1000marcas.net/wp-content/uploads/2024/02/Gemini-Logo.jpg", width=100)
    with tab2:
        st.header("OpenAI - ChatGPT")
        st.image("https://www.androidheadlines.com/wp-content/uploads/2023/03/GPT-4-logo-1420x799.webp",  width=100)
    with tab3:
        st.header("Conversational Data Business ")
        st.image("https://www.researchgate.net/profile/Marianna-Charitonidou/publication/360719662/figure/fig1/AS:1157512099299329@1652983798438/DATA-TUNNEL-2020-21-Custom-software-site-specific-installation-Duration-9-minutes.jpg", width=100)
if selected == "Contact":
    st.title(f"You have selected {selected}")