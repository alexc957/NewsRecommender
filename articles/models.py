from django.db import models
from django.conf import settings
# Create your models here.
from django.utils.timezone import now


class Article(models.Model):
    title = models.CharField(max_length=1000)
    summary = models.TextField()
    lang = models.CharField(max_length=2, default='en')
    category = models.CharField(default='news', null=True, max_length=30)
    date_uploaded = models.DateField(default=now())
    text_vector = models.TextField()


# class Vote(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
#    article  = models.ForeignKey('articles.Article', related_name='vote', on_delete = models.CASCADE)


class SimilarArticle(models.Model):
    principal_article = models.ForeignKey(
        Article, related_name='similar_articles', on_delete=models.CASCADE)
    related_article = models.ForeignKey(
        Article, related_name='similar_to', on_delete=models.CASCADE)
    score = models.FloatField(default=0)


# class Author(models.Model):
#    fullName = models.CharField(max_length=50)

# class AuthorArticle(models.Model):
#    author1 = models.ForeignKey(Author, related_name='articles',on_delete=models.CASCADE)
#    article1 = models.ForeignKey(Article,related_name='authors',on_delete=models.CASCADE)
