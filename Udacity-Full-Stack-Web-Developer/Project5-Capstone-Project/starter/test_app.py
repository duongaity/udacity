import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root123')
DB_NAME = os.getenv('DB_NAME', 'capstone_project')


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)

        self.test_movie = {
            'title': 'Fast & Furious',
            'release_year': 2023
        }

        self.test_actor = {
            'name': 'Vin Diesel',
            'age': 56,
            'gender': 'male',
            'movie_id': 1
        }

        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]

        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables

            self.app.app_context().push()
            self.db.create_all()

    def tearDown(self):
        pass

    # =========================================
    #               Test Get Movie/Actor
    # =========================================

    def test_get_movies(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movies', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_by_director(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/movies', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/actors', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_by_director(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/actors', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_400_get_movies(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movie', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    def test_400_get_actors(self):
        res = self.client().get('/actorrr')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    # =========================================
    #            Test Create Movie
    # =========================================

    def test_create_movie(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post('/movies', json=self.test_movie, headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_400_create_movie(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_fail = {"title": "Movie"}
        res = self.client().post('/movies', json=movie_fail, headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    # =========================================
    #            Test Create Actor
    # =========================================

    def test_create_actor(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().post(f'/actors',
                                 json=self.test_actor, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_create_actor_by_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post(f'/actors',
                                 json=self.test_actor, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_create_actor(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        actor_fail = {"name": "Actor"}
        res = self.client().post(f'/actors',
                                 json=actor_fail, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    # =========================================
    #            Test Update Movie
    # =========================================

    def test_update_movie_by_director(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        new_title = "Eyvah eyvah 2"
        res = self.client().post('/movies', json={
            'title': new_title}, headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie_by_producer(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        new_title = "Eyvah eyvah 1"
        res = self.client().post('/movies', json={
            'title': new_title}, headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_400_update_movie_by_director(self):
        res = self.client().patch('/movies/1', json={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    # =========================================
    #            Test Update Actor
    # =========================================

    def test_update_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        new_actor = {
            'name': "Tom Hanks",
            'age': 54
        }
        res = self.client().patch('/actors/1', json=new_actor, headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_update_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        update_id_actor = 100
        res = self.client().patch(
            f'/actors/{update_id_actor}',
            headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    # =========================================
    #            Test Delete Movie
    # =========================================

    def test_delete_movie(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().delete('/movies/1', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_movie_fail_404(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().delete('/movies/10000', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    # =========================================
    #            Test Delete Actor
    # =========================================

    def test_delete_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().delete('/actors/1', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_delete_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        a_id = -100
        res = self.client().delete(f'/actors/{a_id}', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_403_delete_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().delete('/actors/1', headers=header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
