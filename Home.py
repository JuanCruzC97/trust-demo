import streamlit as st
from src import utils

st.set_page_config(page_title="Home", layout="wide")

# filepath = f'data/label_studio_annotations.json'
# annotations = import_utils.import_label_studio_annotations(filepath, "entities")

corpus = utils.import_corpus_pickle('data/noticias_demo_analizadas.pkl')
title_choices = {index:article.titulo for index, article in corpus.articles.items()}

st.title("Trust")

with st.container(border=True):
    dw_article = st.selectbox('Seleccionar un artículo', (title_choices.keys()), format_func=lambda x: title_choices.get(x))
    
# Get article by index.
article = corpus.get_article(dw_article)

col1, col2 = st.columns([3, 1])

with col1: 
    
    text = article.cuerpo
    html = utils.plot_text(text)   

    st.header(article.titulo)
    st.markdown(html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.metric(label="Medio", value=article.medio)
    with st.container(border=True):
        st.metric(label="Fecha", value=article.fecha)
    with st.container(border=True):
        st.metric(label="Autor", value=article.autor)
    with st.container(border=True):
        st.metric(label="Número de Palabras", value=article.nlp_annotations.doc["stanza"].num_words)

