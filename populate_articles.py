import pandas as pd 
from articles.models import Article
from authors.models import Author
from authorArticle.models import AuthorArticle
from recommendations.Recommender import Recommender 
import spacy 
import sys
from glob import glob
import json 
rec = Recommender() 
filenames = glob('./extracted data/arxiv*')
# en_core_web_lg
nlp =spacy.load('en_core_web_lg')
nlp_es = spacy.load('es_core_news_md')
csv_path = "D:/Projects/UniversityFinalProject/scripts/arxiv_articles.csv"
jsons_path = 'D:/Projects/Spanish news dataset sample/news*'

articles_df = pd.read_csv(csv_path)

# saving first the authors 
def process_text(text):
    doc = nlp_es(text.lower())
    result = []
    for token in doc:
        if token.text in nlp_es.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)

def populate_articles_db():
    #print('saving the the authors')
    #for i,authors in enumerate(articles_df.authors):
    #    for author in authors.split('-'):
    #        current_author = Author.objects.filter(fullName=author).first()
    #        if not current_author:
    #            Author.objects.create(fullName=author)
    #    sys.stdout.write("\r%d%%" % i)
    #    sys.stdout.flush()
        

    # saving the artic
    print("done")
    print('saving articles and creating relations with authors')
    for index,row in articles_df.iterrows():
        
        Article.objects.create(
            title=row['title'],
            summary=row['summary'],
            category=row['main_category'],
            text_vector = ';'.join(nlp(row['summary']).vector.astype(str))
            )

        #article.save()
        article = Article.objects.filter(title=row['title']).first()
        print(article.title)
        #author = Author.objects.filter(fullname=row['authors'])
        authors = row['authors'].split('-')
        for author in authors:
            author_ob = Author.objects.filter(fullName=author).first()
            print(author_ob.fullName)
            author_art  = AuthorArticle(author1 = author_ob, article1 = article)
            author_art.save()
        sys.stdout.write("\r%d%%" % index)
        sys.stdout.flush()

def change_text_vectors():
    all_articles = Article.objects.all() 
    for article in all_articles:
        text_vector =nlp(article.summary).vector
        print(text_vector.shape)
        article.text_vector = ';'.join(text_vector.astype(str))
        article.save()

    print('done')


def save_elcomercio_news():
    #model = spacy.load('es_core_news_md')

    elcomercio_df = pd.read_excel('corpus_elcomercio.xlsx') 
    for index, row in elcomercio_df.iterrows():
        processed_text = process_text(row['Texto'])
        Article.objects.create(
            title = row['Noticia'],
            summary = row['Texto'],
            date_uploaded = row['Fecha'].date(),
            text_vector = ';'.join(nlp_es(processed_text).vector.astype(str))
        )
    print('Done')


def populate_spanish_news():
    filenames = glob(jsons_path)
   
    total_articles = len(filenames)
    
    for i,filename in enumerate(filenames):
        print(f'processsing {i+1} of {5000}')
        with open(filename,encoding='utf8') as file:
            
            data = json.load(file)
            processed_text = process_text(data.get('text'))
            Article.objects.create(
                title = data.get('title'),
                summary = data.get('text'),
                text_vector = ';'.join(nlp_es(processed_text).vector.astype(str))
            )
        if (i==5000):
            break


    print('done')



def change_spanish_vectors():
    all_articles = Article.objects.all() 
    length = len(all_articles)
    for index,article in enumerate(all_articles):
        processed_text = process_text(article.summary)
        article.text_vector = ';'.join(nlp_es(processed_text).vector.astype(str))
        article.save()
        print(f'processed {index + 1 } of {length}') 


