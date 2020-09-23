from django.test import TestCase

# Create your tests here.
from newsgraphql.schema import schema
from django.contrib.auth import get_user_model
from graphene import Context
from graphene.test import Client

client = Client(schema)


class TestUsers(TestCase):
    def setUp(self):
        self.mutation = '''
        mutation {
             createUser(email:"test@mail.com",password:"123", username: "test") {
                user {
                    username
                    }
                }
            }
        '''

        self.expected = {
                "data": {
                    "createUser": {
                        "user": {
                            "username": "test"
                                }
                            }
                        }
                    }
        
    def test_create_user(self):
        executed = client.execute(self.mutation)
        self.assertDictEqual(self.expected,executed)



class QueryUsers(TestCase):
    def setUp(self):
        self.query = '''
        query {
            users {
                username
                    }
                }
        '''

        get_user_model().objects.create(username="test", email='test@test.com')

        self.expected ={
                    "data": {
                        "users": [
                        {
                        "username": "test"
                        }
                    ]
                }
            }

    def test_query_users(self):
        executed = client.execute(self.query)

        self.assertDictEqual(self.expected,executed)