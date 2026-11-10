import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

st.set_page_config(page_title="Opiniones sobre Universidades Peruanas",
                   page_icon="🎓", layout="wide")

nltk.download("stopwords", quiet=True)
STOPS = set(stopwords.words("spanish")) | {"universidad", "universidades", "u", "q", "xq", "pq"}
ETIQUETAS = {"POS": "Positivo", "NEG": "Negativo", "NEU": "Neutro"}
COLORES = {"Negativo": "#d9534f", "Neutro": "#999999", "Positivo": "#5cb85c"}


# ---------- Funciones ----------
@st.cache_resource
def cargar_analizador():
    from pysentimiento import create_analyzer
    return create_analyzer(task="sentiment", lang="es")


def limpiar(texto):
    texto = re.sub(r"http\S+|www\S+", "", str(texto))
    texto = re.sub(r"\d+", "", texto)
    texto = re.sub(r"[^\w\sáéíóúñüÁÉÍÓÚÑÜ]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def palabras_clave(texto):
    return [p for p in limpiar(texto).split() if p not in STOPS and len(p) > 2]


def analizar(textos):
    analizador = cargar_analizador()
    res = analizador.predict([t[:512] for t in textos])
    etiquetas = [ETIQUETAS.get(r.output, r.output) for r in res]
    confianzas = [round(max(r.probas.values()) * 100, 1) for r in res]
    return etiquetas, confianzas


def grafico_sentimiento(df):
    tabla = pd.crosstab(df["universidad"], df["sentimiento"], normalize="index") * 100
    colores = [COLORES.get(c, "#333333") for c in tabla.columns]
    fig, ax = plt.subplots(figsize=(8, 4))
    tabla.plot(kind="bar", stacked=True, ax=ax, color=colores)
    ax.set_ylabel("Porcentaje")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def grafico_nube(df):
    texto = " ".join(" ".join(palabras_clave(t)) for t in df["comentario"])
    if not texto.strip():
        return None
    nube = WordCloud(width=800, height=400, background_color="white").generate(texto)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(nube, interpolation="bilinear")
    ax.axis("off")
    return fig


# ---------- Página ----------
st.title("🎓 Analizador de Opiniones sobre Universidades Peruanas")
st.caption("PC3 - Procesamiento de Lenguaje Natural")

tab1, tab2, tab3 = st.tabs(["📊 Resultados", "✍️ Analizar un comentario", "📁 Subir mi archivo"])

# ----- Pestaña 1: resultados del análisis -----
with tab1:
    try:
        df = pd.read_csv("resultados_analisis.csv")
    except FileNotFoundError:
        df = None
        st.warning("No se encontró el archivo resultados_analisis.csv")

    if df is not None:
        todas = sorted(df["universidad"].unique())
        elegidas = st.multiselect("Universidades", todas, default=todas)
        d = df[df["universidad"].isin(elegidas)]

        if d.empty:
            st.info("Elige al menos una universidad.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Comentarios", len(d))
            c2.metric("Universidades", d["universidad"].nunique())
            c3.metric("% positivos", f"{(d['sentimiento'] == 'Positivo').mean() * 100:.1f}%")

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Sentimiento por universidad")
                st.pyplot(grafico_sentimiento(d))
            with col_b:
                st.subheader("Palabras más usadas")
                fig = grafico_nube(d)
                if fig:
                    st.pyplot(fig)

            if "nombre_tema" in d.columns:
                st.subheader("Temas de conversación por universidad")
                st.bar_chart(pd.crosstab(d["universidad"], d["nombre_tema"]))

            st.subheader("Tabla de comentarios")
            st.dataframe(d, use_container_width=True)

# ----- Pestaña 2: un comentario -----
with tab2:
    st.write("Escribe una opinión sobre una universidad y la analizamos.")
    texto = st.text_area("Comentario", placeholder="Ej: Los profesores son buenos pero los baños están en mal estado")
    if st.button("Analizar comentario"):
        if not texto.strip():
            st.warning("Escribe un comentario primero.")
        else:
            with st.spinner("Analizando..."):
                etiquetas, confianzas = analizar([texto])
            st.metric("Sentimiento", etiquetas[0], f"{confianzas[0]}% de confianza", delta_color="off")
            st.write("**Palabras clave:**", ", ".join(palabras_clave(texto)) or "ninguna")

# ----- Pestaña 3: subir archivo -----
with tab3:
    st.write("Sube un Excel o CSV con las columnas **universidad** y **comentario**.")
    archivo = st.file_uploader("Archivo", type=["xlsx", "csv"])
    if archivo is not None:
        nuevo = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
        if not {"universidad", "comentario"}.issubset(nuevo.columns):
            st.error("El archivo debe tener las columnas 'universidad' y 'comentario'.")
        else:
            nuevo = nuevo.dropna(subset=["comentario"]).reset_index(drop=True)
            st.write(f"Se cargaron {len(nuevo)} comentarios.")
            if st.button("Analizar archivo"):
                with st.spinner("Analizando, puede tardar un poco..."):
                    nuevo["sentimiento"], nuevo["confianza"] = analizar(nuevo["comentario"].astype(str).tolist())
                st.pyplot(grafico_sentimiento(nuevo))
                st.dataframe(nuevo, use_container_width=True)
                st.download_button("Descargar resultados (CSV)",
                                   nuevo.to_csv(index=False).encode("utf-8"),
                                   "resultados.csv", "text/csv")
