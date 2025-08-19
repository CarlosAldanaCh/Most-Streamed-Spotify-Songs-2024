# filename: app.py

"""
Streamlit app para visualizar algunas de las insights para las canciones más escuchadas en Spotify en el año 2024

Requisitos: pip install streamlit pandas plotly
"""
import streamlit as st, pandas as pd, plotly.express as px

# Cargar dataframe

df = pd.read_csv(r"../data/songs_2024.csv", encoding="ISO-8859-1")

st.header("Análisis de las Canciones Más Escuchadas en Spotify 2024")
st.write(
    "Este es un análisis interactivo de las canciones más populares en Spotify durante el año 2024."
)
