# filename: app.py

"""
Streamlit app para visualizar algunas de las insights para las canciones más escuchadas en Spotify en el año 2024

Requisitos: pip install streamlit pandas plotly
"""
import streamlit as st, pandas as pd, plotly.express as px

# page config
st.set_page_config(page_title="Análisis Spotify 2024", layout="wide")

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
# Crear una columna de año de lanzamiento
spotify_df["release_year"] = spotify_df["release_date"].dt.year


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

# Mostrar datos de Spotify
st.subheader("Datos de Spotify")
st.dataframe(spotify_df.head())

# Crear columnas para mejor distribución de los componentes
col1, col2 = st.columns(2)

with col1:
    # Botón para mostrar el gráfico de barras
    bar_button = st.button("Mostrar Top 10 Canciones", key="top_10_songs")

    if bar_button:
        st.write("Creación del Gráfico de Barras con las 10 canciones más escuchadas")
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
                "spotify_streams": "Streams",
                "artist": "Artista",
            },
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Botón para mostrar el histograma de Streams según Popularidad

    hist_button = st.button(
        "Mostrar Histograma de Streams por Popularidad", key="histogram"
    )

    if hist_button:
        st.write("Creación del Histograma de Streams por Popularidad")
        fig = px.histogram(
            spotify_df,
            x="spotify_streams",
            nbins=50,
            color="popularity_bin",
            category_orders={"popularity_bin": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
            title="Streams según Popularidad (1–10)",
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        fig.update_layout(
            xaxis_title="Número de Streams",
            yaxis_title="Número de Canciones",
            legend_title="Popularidad",
        )
        fig.update_traces(marker=dict(line=dict(width=1, color="black")))

        st.plotly_chart(fig, use_container_width=True)

    scatter_button = st.button("Mostrar Gráfico de Dispersión", key="scatter_plot")

    if scatter_button:
        st.write("Creación del Gráfico de Dispersión")
        fig = px.scatter(
            spotify_df,
            x="release_year",
            y="spotify_streams",
            color="popularity_bin",  # para darle un gradiente de color
            size="popularity_bin",  # tamaño según
            category_orders={"popularity_bin": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
            title="Año de Lanzamiento vs Streams(log) en Spotify",
            opacity=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig.update_layout(xaxis_title="Año de Lanzamiento", legend_title="Popularidad")

        fig.update_yaxes(type="log", title="Número de Streams (log)")
        st.plotly_chart(fig, use_container_width=True)


with col2:
    build_bar = st.checkbox("Mostrar Gráfico de Barras", key="bar_plot_check")

    if build_bar:
        st.write("Creación del Gráfico de Barras con las 10 canciones más escuchadas")
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
                "spotify_streams": "Streams",
                "artist": "Artista",
            },
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig, use_container_width=True)

    build_hist = st.checkbox(
        "Mostrar Histograma de Streams por Popularidad", key="histogram_check"
    )

    if build_hist:
        st.write("Creación del Histograma de Streams por Popularidad")
        fig = px.histogram(
            spotify_df,
            x="spotify_streams",
            nbins=50,
            color="popularity_bin",
            category_orders={"popularity_bin": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
            title="Streams según Popularidad (1–10)",
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        fig.update_layout(
            xaxis_title="Número de Streams",
            yaxis_title="Número de Canciones",
            legend_title="Popularidad",
        )
        fig.update_traces(marker=dict(line=dict(width=1, color="black")))

        st.plotly_chart(fig, use_container_width=True)

    build_scatter = st.checkbox(
        "Mostrar Gráfico de Dispersión", key="scatter_plot_check"
    )

    if build_scatter:
        st.write("Creación del Gráfico de Dispersión")
        fig = px.scatter(
            spotify_df,
            x="release_year",
            y="spotify_streams",
            color="popularity_bin",  # para darle un gradiente de color
            size="popularity_bin",  # tamaño según
            category_orders={"popularity_bin": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
            title="Año de Lanzamiento vs Streams(log) en Spotify",
            opacity=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig.update_layout(xaxis_title="Año de Lanzamiento", legend_title="Popularidad")

        fig.update_yaxes(type="log", title="Número de Streams (log)")
        st.plotly_chart(fig, use_container_width=True)
