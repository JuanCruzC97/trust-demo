from spacy import displacy
import pickle




def import_corpus_pickle(filepath):

    with open(filepath, 'rb') as f:
        corpus = pickle.load(f)
        
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