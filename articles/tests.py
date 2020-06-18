from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Article
# Create your tests here.
from pprint import pprint
from newsgraphql.schema import schema
from collector.models import Vote
from graphene.test import Client

import datetime

client = Client(schema)


class ArticleTestCase(TestCase):
    def setUp(self):
        Article.objects.create(
            title="Prueba de busqueda de 2 elementos",
            summary="Esta es una prueba de busqueda de dos elementos",
            lang="es",

        )
        Article.objects.create(
            title="Prueba de busqueda de 2 elementos v2",
            summary="Esta es una prueba de busqueda de dos elementos v2",
            lang="es",

        )
        #print("is setting up? ")

    def test_search_of_articles(self):
        #self.maxDiff = None
        executed = client.execute('''
        query {
                articles(search: "2 elementos") {
                    title
                    summary
                    lang

                }
            } ''')

        expected = {'data': {'articles': [
                    {
                        'title': "Prueba de busqueda de 2 elementos",
                        'summary': "Esta es una prueba de busqueda de dos elementos",
                        'lang': "es"

                    },
                    {
                        'title': "Prueba de busqueda de 2 elementos v2",
                        'summary': "Esta es una prueba de busqueda de dos elementos v2",
                        'lang': "es"
                    },
                    ]
        }
        }

        self.assertTrue(len(executed.get('data').get('articles')) == 2)
        self.assertDictEqual(executed, expected)
        # self.assertEqual


class SearchArticleIdTestCase(TestCase):
    def setUp(self):
        Article.objects.create(
            id=0,
            title="Articulo con ID igual a cero",
            summary="Esta es una prueba de busqueda de un articulo con el ID igual a cero",
            lang="es",

        )

    def test_search_article_with_id(self):
        #id = 0
        expected = {
            "data": {
                "article": {
                    "title": "Articulo con ID igual a cero",
                    "summary": "Esta es una prueba de busqueda de un articulo con el ID igual a cero",
                    "lang": "es"

                }
            }
        }
        executed = client.execute('''
        query {
                article(articleId: 0) {
                    title
                    summary
                    lang

                }
            } ''')
        self.assertDictEqual(executed, expected)


class AddArticleTestCase(TestCase):
    def setUp(self):
        self.expected = {
            "data": {"addArticle": {
                "title": "test insert",
                "summary": "esta una prueba de agregar un nuevo articulo",
                "lang": "es",
                "category": "news",
                "textVector": ""
            }
            }
        }

    def test_add_article(self):
        executed = client.execute(''' 
        mutation {
            addArticle(
            title:"test insert",
            summary:"esta una prueba de agregar un nuevo articulo",
            lang:"es"
            category: "news"
            textVector: ""
    
    
        ){
            title
            summary
            lang
            category
  	        textVector 
        }
        }''')

        self.assertDictEqual(dict(executed.get('data')),
                             self.expected.get('data'))


class RecentArticlesTestCase(TestCase):

    def setUp(self):
        Article.objects.create(
            id=1,
            title="Prueba de busqueda de 2 elementos",
            summary="Esta es una prueba de busqueda de dos elementos",
            lang="es",
            date_uploaded=datetime.date(2020, 8, 22)

        )
        Article.objects.create(
            id=2,
            title="Prueba de busqueda de 2 elementos v2",
            summary="Esta es una prueba de busqueda de dos elementos v2",
            lang="es",
            date_uploaded=datetime.date(2020, 9, 26)

        )

        self.expected = {"data": {
            "recentArticles": [
                {
                    "id": "2"
                },
                {
                    "id": "1"
                }
            ]
        }}

    def test_recent_articles(self):
        executed = client.execute(''' 
        query {
            recentArticles {
                id
            }
        }
        ''')

        self.assertDictEqual(executed, self.expected)


class MostVotedTestCase(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create(
            email="usertest@mail.com",
            password="password1",
            username="usertest"
        )

        user2 = get_user_model().objects.create(
            email="usertest2@mail.com",
            password="password2",
            username="usertest2"
        )
        article1 = Article.objects.create(
            id=1,
            title="Prueba de busqueda de 2 elementos",
            summary="Esta es una prueba de busqueda de dos elementos",
            lang="es",
            date_uploaded=datetime.date(2020, 8, 22)

        )
        article2 = Article.objects.create(
            id=2,
            title="Prueba de busqueda de 2 elementos v2",
            summary="Esta es una prueba de busqueda de dos elementos v2",
            lang="es",
            date_uploaded=datetime.date(2020, 9, 26)

        )
        # creates votes for the second article, 2 votes from user1 and 2 from user2
        for i in range(4):
            Vote.objects.create(
                user=user1 if i < 2 else user2,
                article=article2
            )

        # creates votes for the first article, 2 from user 1 and 1 from user2
        for i in range(3):
            Vote.objects.create(
                user=user1 if i < 2 else user2,
                article=article1
            )
        self.expected = {
            "data": {
                "mostVoted": [
                    {
                        "id": "2"
                    },
                    {
                        "id": "1"
                    }
                ]
            }
        }

    def test_most_voted(self):
        executed = client.execute('''
        query {
            mostVoted {
                id 
                }
            }
        ''')
        self.assertDictEqual(self.expected, executed)
