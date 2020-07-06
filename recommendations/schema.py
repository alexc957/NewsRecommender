import graphene
from graphene_django import DjangoObjectType
from .models import Recommendation
from django.contrib.auth import get_user_model
from users.schema import UserType
from articles.schema import ArticleType
from articles.models import Article, SimilarArticle
from .Recommender import Recommender
from articles.schema import SimilarArticleType
import time
import random 
import datetime 


recommender = Recommender(threshold=0.998)
#recommender2 = Recommender(threshold=0.)
class RecommendationType(DjangoObjectType):
    class Meta: 
        model = Recommendation


class Query(graphene.ObjectType):
    recommendations = graphene.List(
        RecommendationType
        )

    similar_articles = graphene.List(
        SimilarArticleType,
        article_id = graphene.Int(required = True),
    )    

    def resolve_similar_articles(self,info, article_id = None, **kwargs):
        article = Article.objects.filter(id = article_id).first()
        if not article:
            raise Exception("Bad Id provided")
       
        similar_articles = SimilarArticle.objects.filter(principal_article = article).order_by('-score')
    
        #similar_articles = list(similar_articles)
        #random.shuffle(similar_articles)
      
        return similar_articles[:10]

    
    def resolve_recommendations(self, info ,**kwargs):
        user = info.context.user
    
        if not user.is_authenticated:    
        
            raise Exception("You must be logged to receive recommendations")

        
        recommender.generate_recommendations(user) # call the recommender 
        #recommender.generate_recommendations_mult(user)
        recs = Recommendation.objects.filter(user = user).order_by('-score')
        
        
        return recs




class GenerateRecommendations(graphene.Mutation):
    recommendations = graphene.List(RecommendationType)


    def mutate(self,info):

        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged to receive recommendations")
        recommender.generate_recommendations(user) # call the recommender

        return Recommendation.objects.all()[-10:]

class FindSimilarArticles(graphene.Mutation):
    similar_articles = graphene.List(SimilarArticleType)

    class Arguments:
        article_id = graphene.Int()

    def mutate(self,info,article_id):
        article = Article.objects.filter(id = article_id).first()
        if not article:
            raise Exception("Bad Id provided")
        recommender.generate_recommendations_based_on_one_article(article)

        return Recommendation.objects.filter(user = user,recommended=False).order_by('-score')[:10]
        

class Mutation(graphene.ObjectType):
    generate_recommendations = GenerateRecommendations.Field()
    find_similar_articles = FindSimilarArticles.Field()
    
