# Most Streamed Spotify Songs 2024

Aplicación web interactiva construida con **Streamlit**, **Pandas** y **Plotly**, que analiza y visualiza las canciones más escuchadas en Spotify durante el año **2024**.

---

## Funcionalidades

La aplicación incluye:

- **Vista previa de datos**: muestra el dataframe con la información de las canciones.
- **Dos columnas**: se puede elegir entre usar botones o checkboxes para activar las visualizaciones.
- **Top 10 Canciones 2024**: gráfico de barras interactivo con las canciones más reproducidas en Spotify durante 2024.
- **Histograma de Streams por Popularidad**: distribución de streams agrupados en 10 niveles de popularidad.
- **Gráfico de Dispersión (Año vs Streams)**: relación entre el año de lanzamiento y la cantidad de streams, con escala logarítmica en el eje Y.

---

## Tecnologías utilizadas

- [Python 3.x](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/) – manipulación de datos
- [Plotly](https://plotly.com/python/) – visualizaciones interactivas
- [Streamlit](https://streamlit.io/) – desarrollo de la aplicación web

---

## Estructura del proyecto

```bash
.
├── README.md
├── app.py
├── requirements.txt
├── data
│   └── songs_2024.csv
└── notebooks
    └── EDA.ipynb
```

---

## 📖 Notas

- El dataset utilizado es `songs_2024.csv`, con información sobre popularidad, streams, año de lanzamiento y métricas de varias plataformas de streaming, se filtro el dataset para solo trabajar con datos de Spotify.
- El notebook `EDA.ipynb` contiene el análisis exploratorio inicial y los pasos de limpieza, mientras que `app.py` incluye únicamente lo necesario para la visualización.

---

## 👨‍💻 Autor

Desarrollado por **\[Carlos Aldana]** como parte del proyecto práctico del bootcamp de Ciencia de Datos.

---
