import streamlit as st
from src import utils

st.set_page_config(layout="wide")

# ROOT = import_utils.get_project_root()
# filepath = f'{ROOT}/data/manual/label_studio_annotations.json'
# annotations = import_utils.import_label_studio_annotations(filepath, "entities")

filepath = utils.set_data_path()
#corpus = utils.import_corpus_pickle(filepath)
corpus = utils.import_corpus_json(filepath)

title_choices = {article["index"]:article["titulo"] for article in corpus}

st.title("Trust")

with st.container(border=True):
    dw_article = st.selectbox('Seleccionar un artículo', (title_choices.keys()), format_func=lambda x: f'{x} - {title_choices.get(x)}')

#article = corpus.get_article(dw_article)
article = [art for art in corpus if art["index"] == dw_article][0]


col1, col2 = st.columns([3, 1])

with col1: 
    
    text = article["cuerpo"]
    
    sentence_sentiment = article["nlp_annotations"]["sentiment"]['pysentimiento']['sentences']
    sentence_sentiment = [{"label":s["label"], "start_char":s["start_char"], "end_char":s["end_char"]} for s in sentence_sentiment if s["scores"]["NEG"] > 0.8 or s["scores"]["POS"] > 0.8]
    
    sentiment_label = article["nlp_annotations"]["sentiment"]['pysentimiento']['label']
    sentiment_score = article["nlp_annotations"]["sentiment"]['pysentimiento']['scores'][sentiment_label]
    
    entities_sentiment = article["nlp_annotations"]["entities"]["stanza"]
    
    n_entities = len(entities_sentiment)
    prop_sent_pos = sum([e['sentiment'] == 2 for e in entities_sentiment])/n_entities
    prop_sent_neu = sum([e['sentiment'] == 1 for e in entities_sentiment])/n_entities
    prop_sent_neg = sum([e['sentiment'] == 0 for e in entities_sentiment])/n_entities
    
    html = utils.plot_sentence_sentiment(text, sentence_sentiment)   

    st.header(article["titulo"])
    st.markdown(html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.metric(label="Sentimiento General", value=f'{sentiment_label} - {round(sentiment_score, 2)}')
    with st.container(border=True):
        st.metric(label="Proporción Entidades Positivos", value=f'{round(prop_sent_pos*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción Entidades Neutros", value=f'{round(prop_sent_neu*100, 2)} %')
    with st.container(border=True):
        st.metric(label="Proporción Entidades Negativas", value=f'{round(prop_sent_neg*100, 2)} %')
    
    
