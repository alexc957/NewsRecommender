import math
import graphene
from graphene_django import DjangoObjectType

from .models import Article, SimilarArticle
from users.schema import UserType
from django.db.models import Count
#import spacy
from django.db.models import Q
#from recommendations.Recommender import Recommender
#nlp = spacy.load('es_core_news_md')

#recommender = Recommender(threshold=0.95)


class ArticleType(DjangoObjectType):

    class Meta:
        model = Article


class SimilarArticleType(DjangoObjectType):
    class Meta:
        model = SimilarArticle


class Query(graphene.ObjectType):
    articles = graphene.List(
        ArticleType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int())

    article = graphene.Field(
        ArticleType,
        article_id=graphene.Int(required=True)
    )

    recent_articles = graphene.List(ArticleType)

    most_voted = graphene.List(ArticleType)

    total_pages = graphene.Int()

    def resolve_total_pages(self, info, **kwargs):
        all_articles = Article.objects.all()
        total_pages = math.ceil(len(all_articles)/10)
        return total_pages

    def resolve_articles(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Article.objects.all()
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(summary__icontains=search)
            )
            qs = qs.filter(filter)

        print(first)

        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

    def resolve_article(self, info, article_id=None, **kwargs):
        article = Article.objects.get(id=article_id)

        if not article:
            raise Exception('Bad article Id')
        # if not article:
        #    recommender.generate_recommendations_based_on_one_article(article)
        return article

    def resolve_recent_articles(self, info, **kwargs):
        print('hello')
        articles = Article.objects.all().order_by('-date_uploaded')
        return articles[:10]

    def resolve_most_voted(self, info, **kwargs):
        votes = Article.objects.annotate(num_votes=Count('vote'))
        return votes.order_by('-num_votes')[:10]


class AddArticle(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    summary = graphene.String()
    lang = graphene.String()
    category = graphene.String()
    date_uploaded = graphene.Date()
    text_vector = graphene.String()

    class Arguments:
        title = graphene.String()
        summary = graphene.String()
        lang = graphene.String()
        category = graphene.String()
        text_vector = graphene.String()

    def mutate(self, info, title, summary, lang, category, text_vector=None):
        # if not text_vector:
        #text_vector = ';'.join(nlp(summary).vector.astype(str))

        article = Article(
            title=title,
            summary=summary,
            lang=lang,
            category=category,
            text_vector=text_vector
        )

        article.save()

        return AddArticle(
            id=article.id,
            title=article.title,
            summary=article.summary,
            lang=article.lang,
            category=article.category,
            date_uploaded=article.date_uploaded,
            text_vector=article.text_vector


        )


# class CreateVote(graphene.Mutation):
 #   user = graphene.Field(UserType)
  #  article = graphene.Field(ArticleType)

#    class Arguments:
 #       article_id = graphene.Int()

  #  def mutate(self, info, article_id):
   #     user = info.context.user
    #    if user.is_anonymous:
     #       raise Exception('You must be logged to vote!')
      #  article = Article.objects.filter(id = article_id).first()
       # if not article:
       #     raise Exception('Invalid Article')

        # Vote.objects.create(
        #    user = user,
        #    article = article,
        # )

        # return CreateVote(user= user, article = article)


class Mutation(graphene.ObjectType):
    add_article = AddArticle.Field()
    #create_vote = CreateVote.Field()
