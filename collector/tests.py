from django.test import TestCase
from .models import Vote
from newsgraphql.schema import schema
from django.contrib.auth import get_user_model
from graphene.test import Client
from articles.models import Article
from graphene import Context
from pprint import pprint
# Create your tests here.
client = Client(schema)
class QueryVoteTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email = "user@mail.com",
            password = "password",
            username = "user"
        )

        article = Article.objects.create(
            id = 2,
            title = "esta es una prueba",
            summary = "Este es el summary",
            category = "news",
            lang = "es"

        )

        Vote.objects.create(user = self.user, article = article)

        self.expected = {
            "data": {
                "vote": {
                    "user" : {
                        "username": "user"
                    },
                    "article" : {
                        "id": "2"
                    }

                } 

            }
        }
    
    def test_query_vote(self):
        context = Context(user=self.user)
        executed = client.execute('''
        query {
            vote(articleId:2) {
                user {
                  username
                }
                article {
                    id
                }
            }
        }
        ''', context = context )

        self.assertDictEqual(self.expected, executed)

    def test_query_votes(self):
        executed = client.execute('''
        query {
            votes {
                id
                
            }
        }
        ''')
        pprint(executed)
        self.assertDictEqual({
            "data": {
                "votes": [
                    {
                        "id": "1"
                    }
                ]
            }
        },executed)

    def test_create_vote(self):
        context = Context(user=self.user)
        executed = client.execute('''
        mutation {
            createVote(articleId: 2) {
                user {
                    username
                }
                article {
                    id
                }
            }
        }
        ''', context=context)
        expected = {
            "data": {
                "createVote": {
                    "user": {
                        "username": "user"
                    },
                    "article": {
                        "id": 2
                    }
                }
            }
        }

        self.assertDictEqual(expected.get('data'), dic(executed.get('data')))

        






