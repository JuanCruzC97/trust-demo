import streamlit as st
from src import utils

st.set_page_config(layout="wide")

# ROOT = import_utils.get_project_root()
# filepath = f'{ROOT}/data/manual/label_studio_annotations.json'
# annotations = import_utils.import_label_studio_annotations(filepath, "entities")

filepath = utils.set_data_path()
corpus = utils.import_corpus_pickle(filepath)

title_choices = {index:article.titulo for index, article in corpus.articles.items()}

st.title("Trust - Sources")

with st.container(border=True):
    dw_article = st.selectbox('Seleccionar un artículo', (title_choices.keys()), format_func=lambda x: f'{x} - {title_choices.get(x)}')
    
with st.container(border=True):
    dw_source_annotation_type = st.selectbox('Seleccionar un método de anotación', (['simple', 'complete']), format_func=lambda x: x.capitalize())

    #dw_attribute = st.selectbox('Seleccionar un modalidad de detección', ("Automático", "Manual"))

article = corpus.get_article(dw_article)

col1, col2 = st.columns([3, 1])

with col1: 
    
    #text = article.nlp_annotations.doc["spacy_stanza"]  
    #text = article.nlp_annotations.doc["spacy_stanza"].text   #Modificado en el import.
    #tags = article.nlp_annotations.sources["spacy_stanza"]
    text = article.cuerpo
    tags = article.nlp_annotations.sources["stanza"]
    #print(tags)
        
    
    n_sources = len(tags)
    n_sources_con_fuente = len(tags)
    if n_sources > 0:
        prop_sources_con_fuente = n_sources_con_fuente/n_sources
    else:
        prop_sources_con_fuente = 0
    
    
    html = utils.plot_sources(text, tags, annotation_type=dw_source_annotation_type)

    st.header(article.titulo)
    st.markdown(html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.metric(label="Cantidad de Afirmaciones", value=n_sources)
    with st.container(border=True):
        st.metric(label="Cantidad de Afirmaciones con Fuente", value=n_sources_con_fuente)
    with st.container(border=True):
        st.metric(label="Proporción de Afirmaciones con Fuente", value=f'{round(prop_sources_con_fuente*100, 2)} %')
        
    
    
    
