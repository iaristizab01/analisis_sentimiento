import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
import random

st.set_page_config(
    page_title="Analizador Emocional Empático",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Analizador Emocional Empático")
st.markdown("""
Una herramienta que **interpreta el tono emocional de tus palabras**  
y responde con un mensaje empático según la energía que transmite tu texto.
""")

# --- Funciones auxiliares ---
def contar_palabras(texto):
    stop_words = set([
        "a","al","como","con","de","del","el","ella","ellas","ellos","en","es",
        "la","las","los","lo","me","mi","mis","muy","no","nos","o","para",
        "pero","por","que","se","si","sin","su","sus","te","tu","tus","un","una",
        "uno","y","ya","yo"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for p in palabras_filtradas:
        contador[p] = contador.get(p, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

def traducir_texto(texto):
    try:
        traduccion = TextBlob(texto).translate(to='en')
        return str(traduccion)
    except:
        return texto

def procesar_texto(texto):
    texto_traducido = traducir_texto(texto)
    blob = TextBlob(texto_traducido)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    contador_palabras = contar_palabras(texto_traducido)
    return {
        "texto_original": texto,
        "texto_traducido": texto_traducido,
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador_palabras": contador_palabras
    }

# --- Respuesta empática ---
def generar_respuesta(sentimiento):
    if sentimiento > 0.2:
        mensajes = [
            "Se siente una energía positiva en tu texto 😊",
            "Tu mensaje transmite optimismo y buena vibra ✨",
            "Parece un texto con emociones alegres y esperanzadoras 🌞"
        ]
    elif sentimiento < -0.2:
        mensajes = [
            "Tu texto refleja algo de tristeza o preocupación 💭",
            "Parece un mensaje con una carga emocional más pesada 😔",
            "Hay un tono sensible, quizá una emoción difícil detrás 💙"
        ]
    else:
        mensajes = [
            "El texto se percibe bastante equilibrado 😌",
            "No hay emociones muy fuertes, suena neutral o reflexivo 🪞",
            "Parece un mensaje tranquilo, sin extremos 💬"
        ]
    return random.choice(mensajes)

# --- Visualización ---
def mostrar_resultados(resultados):
    st.subheader("🎭 Análisis Emocional")
    st.write(f"**Sentimiento:** {resultados['sentimiento']:.2f}")
    st.write(f"**Subjetividad:** {resultados['subjetividad']:.2f}")

    st.markdown("### 💬 Interpretación del tono")
    st.info(generar_respuesta(resultados["sentimiento"]))

    st.subheader("📖 Traducción automática")
    st.text_area("Texto traducido al inglés", resultados["texto_traducido"], height=150)

    st.subheader("🔠 Palabras más frecuentes")
    top_words = dict(list(resultados["contador_palabras"].items())[:10])
    if top_words:
        st.bar_chart(top_words)
    else:
        st.write("No se encontraron palabras significativas.")

# --- Interfaz principal ---
st.sidebar.title("⚙️ Opciones")
modo = st.sidebar.selectbox("Selecciona el modo de entrada:", ["Texto directo", "Archivo de texto"])

if modo == "Texto directo":
    st.subheader("🖋️ Escribe tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe algo y descubre qué emoción transmite...")
    
    if st.button("Analizar texto 💬"):
        if texto.strip():
            with st.spinner("Analizando emociones..."):
                resultados = procesar_texto(texto)
                mostrar_resultados(resultados)
        else:
            st.warning("Por favor, escribe algo para analizar.")

else:
    st.subheader("📁 Carga un archivo de texto (.txt)")
    archivo = st.file_uploader("", type=["txt"])
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        st.text_area("Vista previa del archivo:", contenido[:500] + ("..." if len(contenido) > 500 else ""))
        if st.button("Analizar archivo 💬"):
            with st.spinner("Leyendo el texto..."):
                resultados = procesar_texto(contenido)
                mostrar_resultados(resultados)

st.markdown("---")
st.markdown("Desarrollado con empatía 💙 por *Isabela Aristizábal*")
