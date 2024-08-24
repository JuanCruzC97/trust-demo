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

st.title("Trust - Entities")

with st.container(border=True):
    dw_article = st.selectbox('Seleccionar un artículo', (title_choices.keys()), format_func=lambda x: f'{x} - {title_choices.get(x)}')

    #dw_attribute = st.selectbox('Seleccionar un modalidad de detección', ("Automático", "Manual"))
    dw_attribute = "Automático"

#article = corpus.get_article(dw_article)
print([art for art in corpus if art["index"] == dw_article])
article = [art for art in corpus if art["index"] == dw_article][0]

col1, col2 = st.columns([3, 1])

with col1: 
    
    #text = article.cuerpo
    text = article["cuerpo"]
    
    if dw_attribute == "Automático":
        #tags = article.nlp_annotations.entities["stanza"]
        tags = article["nlp_annotations"]["entities"]["stanza"]
        
    else:
        #tags = article.manual_annotations['entities']
        tags = article["manual_annotations"]["entities"]
        
    
    n_entities = article["nlp_annotations"]["metrics"]["entities"]["num_entidades"]["value"]
    #prop_entities = n_entities/article.nlp_annotations.doc["stanza"].num_words
    prop_entities_per = article["nlp_annotations"]["metrics"]["entities"]["num_entidades_persona"]["value"]/n_entities
    prop_entities_lug = article["nlp_annotations"]["metrics"]["entities"]["num_entidades_lugar"]["value"]/n_entities
    prop_entities_org = article["nlp_annotations"]["metrics"]["entities"]["num_entidades_organizacion"]["value"]/n_entities
    prop_entities_misc = article["nlp_annotations"]["metrics"]["entities"]["num_entidades_misc"]["value"]/n_entities
    
    tagged_text = utils.plot_entities(text, tags)   

    #st.header(article.titulo)
    st.header(article["titulo"])
    st.markdown(tagged_text, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.metric(label="Cantidad de Entidades", value=n_entities)
    #with st.container(border=True):
    #    st.metric(label="Porporción de Entidades", value=f'{round(prop_entities*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción de Personas", value=f'{round(prop_entities_per*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción de Lugar", value=f'{round(prop_entities_lug*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción de Organización", value=f'{round(prop_entities_org*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción de Misceláneo", value=f'{round(prop_entities_misc*100, 2)} %')
        
    
    
    
