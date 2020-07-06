#import spacy
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from collector.models import Vote
from articles.models import Article, SimilarArticle
from .models import Recommendation
from multiprocessing import Process
import multiprocessing
import time
import threading


import numpy as np
import random
import django
# django.setup()


class Recommender:

    def __init__(self, lang='en', threshold=0.99):
        #self.model = spacy.load('en_core_web_lg')
        self.threshold = threshold
        self.lang = lang

    def cosine_similarity_score(self, x, y):
        y = np.array(y.split(';')).astype(float)
        x = np.array(x.split(';')).astype(float)
        # print(y.shape)
        # print(x.shape)
        try:

            similarity_score = cosine_similarity([x], [y])
        except ValueError:
            return 0

        if similarity_score.size > 0:
            return similarity_score[0, 0]
        return 0

    def find_most_significant_article(self, articles, liked_article):
        top_ten_similar_article = []
        num_articles_with_score_above_trehshold = 0
        # print('called')
        for article in articles:
            similarity = self.cosine_similarity_score(
                liked_article.text_vector,
                article.text_vector
            )
            #print('similarity', similarity)
            #print('sim type', type(similarity))

            if similarity > self.threshold:
                top_ten_similar_article.append((article, similarity))
                # print((article.id,similarity))
                num_articles_with_score_above_trehshold += 1

            if num_articles_with_score_above_trehshold > 10:
                break
        # if not top_ten_similar_article:
        #    return None
        # most_revelant_article = sorted(
         #   article_score_pair, key= lambda x: x[1], reverse=True
        # )[0]

        # print(most_revelant_article[0])
        #article = Article.objects.filter(id = most_revelant_article[0]).first()
        return top_ten_similar_article
        # return (article, most_revelant_article[1])

        # if len(article_score_pair)==0:
        #    return None

    def generate_recommendations(self, user):
        """
            Genera recomendaciones en base al votos/perfil de usuario 
        """
        votes_made_by_user = Vote.objects.filter(user=user, liked=True)

        articles_liked_by_user = [vote.article for vote in votes_made_by_user]
        for article_liked in articles_liked_by_user:
            for similar_article in article_liked.similar_articles.all()[:5]:
                recommendation = Recommendation.objects.filter(
                    article=similar_article.related_article, user=user).first()
                if not recommendation:
                    Recommendation.objects.create(
                        score=similar_article.score,
                        user=user,
                        article=similar_article.related_article

                    )
        print("done")

    # def get_top_ten_recommendations(self, user):
     #   return Recommendation.objects.filter(user=user).order_by('score')

    def generate_recommendations_based_on_one_article(self, current_article):
        all_articles = list(Article.objects.all())
        random.shuffle(all_articles)
        print(f'was suffle the list? {all_articles[0].id}')

        count_recs = 0
        # print(len(all_articles))
        for article in all_articles:
            similarity_score = self.cosine_similarity_score(
                current_article.text_vector, article.text_vector)

            if similarity_score > self.threshold:
                # print(similarity_score)
                similar_article = SimilarArticle.objects.filter(
                    principal_article=current_article, related_article=article).first()
                if not similar_article:

                    similar_article = SimilarArticle(
                        principal_article=current_article, related_article=article)
                    similar_article.save()
                    # print(similar_article.principal_article.title)
                    count_recs += 1
            if count_recs > 9:
                break
        print('done')

    def find_similars_articles_in_all_articles(self):
        all_articles = Article.objects.all()
        t0 = time.time()
        length = len(all_articles)
        for idx in range(2224, length):
            print(f"processing {idx+1} of {length} ")
            for article_a in all_articles:
                if all_articles[idx] != article_a.id:
                    sim_score = self.cosine_similarity_score(
                        all_articles[idx].text_vector, article_a.text_vector)
                    similar_article = SimilarArticle.objects.filter(
                        principal_article=all_articles[idx], related_article=article_a).first()

                    if sim_score > self.threshold and not similar_article:
                        #print("creating similar article")
                        SimilarArticle.objects.create(
                            principal_article=all_articles[idx],
                            related_article=article_a,
                            score=similar_article,
                        )
        print("done")
        print(f'total time: {(time.time() - t0)/60} minutes')
