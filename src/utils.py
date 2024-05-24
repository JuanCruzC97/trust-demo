from spacy import displacy
import streamlit as st
from io import StringIO
import pickle
from trustmonitor import import_utils


ROOT = import_utils.get_project_root()

# Por ahora cambiando el default se aplica en todas las páginas.
# Esto debería ser una variable de configuración.
@st.cache_resource
def set_data_path(v: int=3):
    
    if v == 1:
        return 'data/v1/noticias_demo_analizadas.pkl'
    elif v == 2:
        return 'data/v2/corpus_lavoz_politica_negocios_nlp_srcs.pkl'
    elif v == 3:
        return 'data/v3/corpus_lavoz_politica_negocios_5_srcs.pkl'
        #return f"{ROOT}/data/pickle_files/corpus_lavoz_politica_negocios_5_srcs.pkl"
    
    
    return None


#@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
@st.cache_resource
def import_corpus_pickle(filepath):
    
    if filepath is None:
        raise ValueError("Filepath is None.")

    with open(filepath, 'rb') as f:
        corpus = pickle.load(f)
        
    # for article in corpus.get_articles():
    #     for k in article.nlp_annotations.doc.keys():
    #         if k == "spacy_stanza":
    #             article.nlp_annotations.doc[k] = article.nlp_annotations.doc[k].text
    #         else:
    #             article.nlp_annotations.doc[k] = None
        
    return corpus



def plot_text(text):
    
    plot_data = {"text": text, "ents": [], "title": None}
        
    html = displacy.render(plot_data, style="ent", manual=True, jupyter=False)
    return html


def plot_entities(text, entities):
    
    options = {'colors':{"Persona":"#fcba03", "Lugar":"#22B8C3", "Misceláneo":"#E421D3", "Organización":"#22BF51"}}
        
    plot_data = {"text": text,
            "ents": [{'start':e['start_char'], 'end':e['end_char'], 'label':e['type']} for e in entities],
            "title": None
            }

    html = displacy.render(plot_data, style="ent", manual=True, jupyter=False, options=options)
    return html


def plot_adjectives(text, adjectives):
    
    options = {'colors':{a['type']:"#fcba03" for a in adjectives}}
        
    plot_data = {"text": text,
            "ents": [{'start':a['start_char'], 'end':a['end_char'], 'label':a['type']} for a in adjectives],
            "title": None
            }

    html = displacy.render(plot_data, style="ent", manual=True, jupyter=False, options=options)
    return html


def plot_entities_sentiment(text, entities):
    
    options = {'colors':{"NEG":"#F95224", "NEU":"#fcba03", "POS":"#22BF51"}}
    labels = {0:"NEG", 1:"NEU", 2:"POS"}
    
    plot_data = {"text": text,
            "ents": [{'start':a['start_char'], 'end':a['end_char'], 'label':labels[a['sentiment']]} for a in entities],
            "title": None
            }

    html = displacy.render(plot_data, style="ent", manual=True, jupyter=False, options=options)
    return html


def plot_sources(text, sources_list, annotation_type: str="simple"):
    
    options = {'colors':{"Fuente":"#ffd642", "Afirmacion":"#ffd642", "Conector":"#f55d32", "Referenciado":"#59d8f7", "Afirmacion Debil":"#ef9eff"}}
    
    if annotation_type == 'simple':
        sources_to_plot = [{'start':s['start_char'], 'end':s['end_char'], 'label':'Fuente'} for s in sources_list]
    
    elif annotation_type == 'complete':
        sources_to_plot = [{'start':c['start_char'], 'end':c['end_char'], 'label':c['label']} for s in sources_list for c in s["components"].values()]
        
    else:
        raise ValueError("Invalid annotation type")
        
    plot_data = {"text": text,
                 "ents": sources_to_plot,
                 "title": None
                 }
    
    #print(sources_list)

    html = displacy.render(plot_data, style="ent", manual=True, jupyter=False, options=options)
    return html