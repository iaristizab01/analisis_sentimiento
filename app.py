import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📝 Analizador de Texto con TextBlob")
st.markdown("""
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:
- Análisis de sentimiento y subjetividad  
- Traducción automática  
- Frecuencia de palabras más usadas
""")

# Barra lateral
st.sidebar.title("Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# Función para contar palabras
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

# Función para traducir texto con TextBlob
def traducir_texto(texto):
    try:
        traduccion = TextBlob(texto).translate(to='en')
        return str(traduccion)
    except Exception as e:
        st.warning(f"No se pudo traducir automáticamente: {e}")
        return texto

# Procesamiento principal
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

# Mostrar resultados
def mostrar_resultados(resultados):
    st.subheader("🎭 Análisis de Sentimiento")
    st.write(f"**Sentimiento:** {resultados['sentimiento']:.2f}")
    st.write(f"**Subjetividad:** {resultados['subjetividad']:.2f}")
    
    if resultados["sentimiento"] > 0.05:
        st.success("El texto tiene un tono positivo 😄")
    elif resultados["sentimiento"] < -0.05:
        st.error("El texto tiene un tono negativo 😟")
    else:
        st.info("El texto es neutral 😐")
    
    st.subheader("📖 Traducción automática")
    st.text_area("Texto traducido al inglés", resultados["texto_traducido"], height=150)
    
    st.subheader("🔠 Palabras más frecuentes")
    top_words = dict(list(resultados["contador_palabras"].items())[:10])
    if top_words:
        st.bar_chart(top_words)
    else:
        st.write("No se encontraron palabras significativas.")

# Modo de texto directo
if modo == "Texto directo":
    st.subheader("✏️ Ingresa tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")
    
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando texto..."):
                resultados = procesar_texto(texto)
                mostrar_resultados(resultados)
        else:
            st.warning("Por favor, escribe algo para analizar.")

# Modo de archivo
else:
    st.subheader("📁 Carga un archivo de texto (.txt)")
    archivo = st.file_uploader("", type=["txt"])
    
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        st.text_area("Vista previa del archivo:", contenido[:500] + ("..." if len(contenido) > 500 else ""))
        if st.button("Analizar archivo"):
            with st.spinner("Analizando archivo..."):
                resultados = procesar_texto(contenido)
                mostrar_resultados(resultados)

st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Streamlit y TextBlob")

