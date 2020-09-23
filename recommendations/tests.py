from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article, SimilarArticle
from recommendations.models import Recommendation 
from graphene import Context
from newsgraphql.schema import schema
from graphene.test import Client
# Create your tests here.

client = Client(schema)

class RecommendationsTestCases(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create(
            email = "user@mail.com",
            password = "password",
            username = "user"
        )
        self.article1 = Article.objects.create(
            id=1,
            title='article 1',
            summary='this is a summary',
            lang='es')
        self.article2 = Article.objects.create(
            id=2,
            title='article 2',
            summary='this is a summary v2',
            lang='es')

        self.article3 = Article.objects.create(
            id=3,
            title='article 3',
            summary='this is a summary v3',
            lang='es')
        SimilarArticle.objects.create(principal_article=self.article1,related_article=self.article2)
        SimilarArticle.objects.create(principal_article=self.article1,related_article=self.article3)
         
        Recommendation.objects.create(
                        id=1,
                        score=0.95,
                        user=self.user,
                        article=self.article2

                    )

        Recommendation.objects.create(
                        id=2,
                        score=0.91,
                        user=self.user,
                        article=self.article3

                    )

        self.context = Context(user=self.user)

        


        
    def test_query_similar_articles(self):
        executed = client.execute('''
        {
            similarArticles(articleId: 1) {
    		    relatedArticle {
                    id
                }
             }
        }
        ''',context=self.context)

        expected = {
            "data":  {
                "similarArticles": [
                    {'relatedArticle': {"id":'2'}},
                    {'relatedArticle': {"id":'3'}}
                    
                ]
            }          
            
        }

        self.assertDictEqual(expected,executed)



    def test_query_recommendations(self):
        executed = client.execute('''
        {
         recommendations {
            id
    
            }
        }''',context=self.context)

        expected = {
            "data": {
                "recommendations" : [
                    {"id":"1"},
                    {"id":"2"}
                ]
            } 
            
        }

        self.assertDictEqual(expected,executed)
        



    

    

    

