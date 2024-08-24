import streamlit as st
from src import utils

st.set_page_config(layout="wide")

# ROOT = import_utils.get_project_root()
# filepath = f'{ROOT}/data/manual/label_studio_annotations.json'
# annotations = import_utils.import_label_studio_annotations(filepath, "entities")

filepath = utils.set_data_path()
#corpus = utils.import_corpus_pickle(filepath)
corpus = utils.import_corpus_json(filepath)

#title_choices = {index:article.titulo for index, article in corpus.articles.items()}
title_choices = {article["index"]:article["titulo"] for article in corpus}

st.title("Trust - Adjectives")

with st.container(border=True):
    dw_article = st.selectbox('Seleccionar un artículo', (title_choices.keys()), format_func=lambda x: f'{x} - {title_choices.get(x)}')

#article = corpus.get_article(dw_article)
article = [art for art in corpus if art["index"] == dw_article][0]

#text = article.cuerpo
text = article["cuerpo"]

adjectivos = article["nlp_annotations"]["adjectives"]["stanza"]

tagged_text = utils.plot_adjectives(text, adjectivos)

n_adjetivos = article["nlp_annotations"]["metrics"]["adjectives"]["num_adjectives"]["value"]
n_words = article["nlp_annotations"]["metrics"]["general"]["num_words"]["value"]
prop_adjetivos = n_adjetivos/n_words

col1, col2 = st.columns([3, 1])

with col1: 

    st.header(article["titulo"])
    st.markdown(tagged_text, unsafe_allow_html=True)
    
with col2:
    with st.container(border=True):
        st.metric(label="Cantidad de Adjetivos", value=n_adjetivos)
    with st.container(border=True):
        st.metric(label="Proporción de Adjetivos", value=f'{round(prop_adjetivos*100, 2)} %')
