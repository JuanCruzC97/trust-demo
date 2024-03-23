from trustmonitor import import_utils
from trustmonitor.articles import ArticlesCorpus
from trustmonitor.nlp import NLP

def main():
    corpus = ArticlesCorpus()
    noticias = import_utils.import_news_from_json(f"trust-demo/data/noticias_demo.json")
    corpus.load_articles(noticias)

    nlp = NLP(language="es", libreria="stanza")
    nlp.analyze_corpus_cuerpo(corpus)

    nlp = NLP(language="es", libreria="spacy")
    nlp.analyze_corpus_cuerpo(corpus)

    nlp = NLP(language="es", libreria="pysentimiento")
    nlp.analyze_corpus_cuerpo(corpus)
    nlp._extract_corpus_sentiment(corpus)

    filepath = f'trust-demo/data/label_studio_annotations.json'
    annotations = import_utils.import_entities_manual_annotations(filepath)

    for art in corpus.articles.values():
        for ann in annotations:
            if ann["titulo"] == art.titulo:
                art.manual_annotations = {'entities': ann['entities']}
                
    # Add metrics in new article attribute.

    #print(corpus.get_article(0).nlp_annotations.__dict__)

    corpus.save_corpus("trust-demo/data/noticias_demo_analizadas.pkl")
    
if __name__ == "__main__":
    main()