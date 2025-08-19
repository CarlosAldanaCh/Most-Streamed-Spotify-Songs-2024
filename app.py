# filename: app.py

"""
Streamlit app para visualizar algunas de las insights para las canciones más escuchadas en Spotify en el año 2024

Requisitos: pip install streamlit pandas plotly
"""
import streamlit as st, pandas as pd, plotly.express as px

# Cargar dataframe

df = pd.read_csv(r"./data/songs_2024.csv", encoding="ISO-8859-1")

st.header("Análisis de las Canciones Más Escuchadas en Spotify 2024")
st.write(
    "Este es un análisis interactivo de las canciones más populares en Spotify durante el año 2024."
)

# Filtrar solo las columnas necesarias para trabajar solo con datos de Spotify
filtered_columns = [col for col in df.columns if "spotify" in col.lower()]
spotify_df = df[
    ["Track", "Album Name", "Artist", "Release Date", "All Time Rank", "Track Score"]
    + filtered_columns
]


spotify_df.columns = spotify_df.columns.str.lower().str.replace(" ", "_", regex=False)

# Limpieza de datos nulos en las columnas importantes
spotify_df = spotify_df.dropna(subset=["artist", "spotify_streams"])
spotify_df["track"] = spotify_df["track"].drop_duplicates()
spotify_df = spotify_df.dropna(subset=["track"])

# Cambiar tipo de dato de 'release_date' a datetime
spotify_df["release_date"] = pd.to_datetime(spotify_df["release_date"], errors="coerce")

# Cambiar tipo de dato de 'spotify_streams' a int
spotify_df["spotify_streams"] = spotify_df["spotify_streams"].str.replace(",", "")
spotify_df["spotify_streams"] = spotify_df["spotify_streams"].astype(int)

# Crear bins para la popularidad de las canciones de 1-10
spotify_df["popularity_bin"] = pd.cut(
    spotify_df["spotify_popularity"],
    bins=10,  # 10 intervalos iguales
    labels=range(1, 11),  # etiquetas 1–10
    ordered=True,
)

# Top 10 canciones más escuchadas del 2024
top_10_songs = (
    spotify_df[spotify_df["release_year"] == 2024]
    .nlargest(10, "spotify_streams")
    .sort_values(by="spotify_streams", ascending=False)
)
order = top_10_songs["track"].tolist()
top_10_songs["track"] = pd.Categorical(
    top_10_songs["track"], categories=order, ordered=True
)
order_rev = order[::-1]

bar_button = st.button("Mostrar Top 10 Canciones", key="top_10_songs")

if bar_button:
    st.write("Top 10 Canciones Más Escuchadas en Spotify 2024")
    fig = px.bar(
        top_10_songs,
        y="track",
        x="spotify_streams",
        orientation="h",
        color="artist",
        category_orders={"track": order_rev},
        title="Top 10 Canciones Más Escuchadas en 2024",
        labels={
            "track": "Canción",
            "spotify_streams": "Número de Streams",
            "artist": "Artista",
        },
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig, use_container_width=True)
