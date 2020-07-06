from .models import Article
import pandas as pd 

def populate_db():

    news_articles = pd.read_csv('./articles/allthenews.csv')

    for index, row in news_articles.iterrows():
        article = Article(title = row['title'], content = row['text'],lang = 'en', text_vector = row['text_vector'])
        article.save()

    print('done')