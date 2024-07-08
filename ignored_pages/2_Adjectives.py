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


adjectives = []
doc = article.nlp_annotations.doc["stanza"]

for sentence in doc.sentences:
    for word in sentence.words:
        if word.upos == 'ADJ':
            adejctive_text = word.text
            adejctive_start = word.start_char
            adejctive_end = word.end_char
            adjectives_xpos = word.xpos
            adjective_features = {}
            if word.feats is not None:
                feats = word.feats.split("|")
                for feat in feats:
                    key, value = feat.split("=")
                    adjective_features[key] = value
            adjectives.append({
                'text': adejctive_text,
                'start_char':adejctive_start,
                'end_char':adejctive_end,
                'type':f'ADJ-{adjectives_xpos}',
                'features': adjective_features
            })


html = utils.plot_adjectives(text, adjectives)
n_adjetivos = len(adjectives)
prop_adjetivos = n_adjetivos/article.nlp_annotations.doc["stanza"].num_words

col1, col2 = st.columns([3, 1])

with col1: 

    st.header(article.titulo)
    st.markdown(html, unsafe_allow_html=True)
    
with col2:
    with st.container(border=True):
        st.metric(label="Cantidad de Adjetivos", value=n_adjetivos)
    with st.container(border=True):
        st.metric(label="Proporción de Adjetivos", value=f'{round(prop_adjetivos*100, 2)} %')
