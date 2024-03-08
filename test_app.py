import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from app import create_app
from datetime import datetime
from database.models import setup_db, Actor, Movie

MESSAGE_400 = "bad request"
MESSAGE_401 = "Authorization header is expected"
MESSAGE_403 = "Permission not found"
MESSAGE_404 = "Resource not found"
MESSAGE_500 = "Internal server error"


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = ('postgresql://postgres:postgres@{}/{}'
                              .format('localhost:5432', self.database_name))

        f = open('auth_config.json')
        auth_config = json.load(f)

        casting_assistant_token = auth_config['casting_assistant_token']
        casting_director_token = auth_config['casting_director_token']
        executive_producer_token = auth_config['executive_producer_token']

        self.casting_assistant_header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(casting_assistant_token)
        }
        self.casting_director_header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(casting_director_token)
        }
        self.executive_producer_header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(executive_producer_token)
        }
        setup_db(self.app, self.database_path)

        self.faker = Faker()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Casting Assistant
    """

    def test_casting_assistant_retrieve_actors(self):
        res = self.client().get('/api/actors',
                                content_type='application/json',
                                headers=self.casting_assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_casting_assistant_retrieve_movies(self):
        res = self.client().get('/api/movies',
                                content_type='application/json',
                                headers=self.casting_assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_casting_assistant_create_actors_401(self):
        actor = {
            'name': self.faker.name(),
            'age': 25,
            'gender': 'male'
        }
        res = self.client().post('/api/actors',
                                 content_type='application/json',
                                 json=actor)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], MESSAGE_401)
        self.assertEqual(data['success'], False)

    def test_casting_assistant_create_actors_403(self):
        actor = {
            'name': self.faker.name(),
            'age': 25,
            'gender': 'male'
        }
        res = self.client().post('/api/actors',
                                 content_type='application/json',
                                 json=actor,
                                 headers=self.casting_assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], MESSAGE_403)
        self.assertEqual(data['success'], False)

    """
    Casting Director
    """

    def test_casting_director_retrieve_actors(self):
        res = self.client().get('/api/actors',
                                content_type='application/json',
                                headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_casting_director_create_actors(self):
        actor = {
            'name': self.faker.name(),
            'age': 30,
            'gender': 'male'
        }
        res = self.client().post('/api/actors',
                                 content_type='application/json',
                                 json=actor,
                                 headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], actor['age'])
        self.assertEqual(data['actor']['gender'], actor['gender'])
        self.assertEqual(data['actor']['name'], actor['name'])

    def test_casting_director_update_actors(self):
        existing_actor = Actor.query.order_by(Actor.id.desc()).limit(1).first()
        actor = {
            'name': existing_actor.name,
            'age': existing_actor.age + 5,
            'gender': existing_actor.gender
        }
        res = self.client().patch(f'/api/actors/{existing_actor.id}',
                                  content_type='application/json',
                                  json=actor,
                                  headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], existing_actor.id)
        self.assertEqual(data['actor']['age'], actor['age'])
        self.assertEqual(data['actor']['gender'], actor['gender'])
        self.assertEqual(data['actor']['name'], actor['name'])

    def test_casting_director_delete_actors(self):
        existing_actor = Actor.query.order_by(Actor.id.desc()).limit(1).first()
        res = self.client().delete(f'/api/actors/{existing_actor.id}',
                                   content_type='application/json',
                                   headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], existing_actor.id)
        self.assertEqual(data['actor']['age'], existing_actor.age)
        self.assertEqual(data['actor']['gender'], existing_actor.gender)
        self.assertEqual(data['actor']['name'], existing_actor.name)

    def test_casting_director_retrieve_movies(self):
        res = self.client().get('/api/movies',
                                content_type='application/json',
                                headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_casting_director_create_movies_403(self):
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().post('/api/movies',
                                 content_type='application/json',
                                 json=movie,
                                 headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], MESSAGE_403)
        self.assertEqual(data['success'], False)

    def test_casting_director_update_movies(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().patch(f'/api/movies/{existing_movie.id}',
                                  content_type='application/json',
                                  json=movie,
                                  headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], existing_movie.id)
        self.assertEqual(data['movie']['release_date'], movie['release_date'])
        self.assertEqual(data['movie']['title'], movie['title'])

    def test_casting_director_update_movies_404(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().patch(f'/api/movies/{existing_movie.id + 1}',
                                  content_type='application/json',
                                  json=movie,
                                  headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], MESSAGE_404)
        self.assertEqual(data['success'], False)

    def test_casting_director_delete_movie_403(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        res = self.client().delete(f'/api/movies/{existing_movie.id}',
                                   content_type='application/json',
                                   headers=self.casting_director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_403)

    """
    Executive Producer
    """

    def test_executive_producer_retrieve_actors(self):
        res = self.client().get('/api/actors',
                                content_type='application/json',
                                headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_executive_producer_create_actors(self):
        actor = {
            'name': self.faker.name(),
            'age': 25,
            'gender': 'female'
        }
        res = self.client().post('/api/actors',
                                 content_type='application/json',
                                 json=actor,
                                 headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], actor['age'])
        self.assertEqual(data['actor']['gender'], actor['gender'])
        self.assertEqual(data['actor']['name'], actor['name'])

    def test_executive_producer_update_actors(self):
        existing_actor = Actor.query.order_by(Actor.id.desc()).limit(1).first()
        actor = {
            'name': existing_actor.name,
            'age': existing_actor.age + 5,
            'gender': existing_actor.gender
        }
        res = self.client().patch(f'/api/actors/{existing_actor.id}',
                                  content_type='application/json',
                                  json=actor,
                                  headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], existing_actor.id)
        self.assertEqual(data['actor']['age'], actor['age'])
        self.assertEqual(data['actor']['gender'], actor['gender'])
        self.assertEqual(data['actor']['name'], actor['name'])

    def test_executive_producer_delete_actors(self):
        existing_actor = Actor.query.order_by(Actor.id.desc()).limit(1).first()
        res = self.client().delete(f'/api/actors/{existing_actor.id}',
                                   content_type='application/json',
                                   headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], existing_actor.id)
        self.assertEqual(data['actor']['age'], existing_actor.age)
        self.assertEqual(data['actor']['gender'], existing_actor.gender)
        self.assertEqual(data['actor']['name'], existing_actor.name)

    def test_executive_producer_retrieve_movies(self):
        res = self.client().get('/api/movies',
                                content_type='application/json',
                                headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_executive_producer_create_movies(self):
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().post('/api/movies',
                                 content_type='application/json',
                                 json=movie,
                                 headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'], movie['release_date'])
        self.assertEqual(data['movie']['title'], movie['title'])

    def test_executive_producer_update_movies(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().patch(f'/api/movies/{existing_movie.id}',
                                  content_type='application/json',
                                  json=movie,
                                  headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], existing_movie.id)
        self.assertEqual(data['movie']['release_date'], movie['release_date'])
        self.assertEqual(data['movie']['title'], movie['title'])

    def test_executive_producer_update_movies_404(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        movie = {
            'title': self.faker.sentence(),
            'release_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        res = self.client().patch(f'/api/movies/{existing_movie.id + 1}',
                                  content_type='application/json',
                                  json=movie,
                                  headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], MESSAGE_404)
        self.assertEqual(data['success'], False)

    def test_executive_producer_delete_movie(self):
        existing_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
        res = self.client().delete(f'/api/movies/{existing_movie.id}',
                                   content_type='application/json',
                                   headers=self.executive_producer_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], existing_movie.id)
        self.assertEqual(data['movie']['release_date'],
                         existing_movie.release_date
                         .strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data['movie']['title'], existing_movie.title)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
