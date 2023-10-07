from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, True')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH, OPTIONS')
        return response
    
    @app.route('/', methods=['GET'])
    def first_app():
        return jsonify({
            'success': True,
            'description': 'App is running.'
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(f):
        movies = Movie.query.all()

        if not movies:
            abort(404)

        movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": movies
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(f):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not (title and release_date):
            abort(422)

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify({
                    'success': True,
                    'movie_id': movie.format()
                })
        except:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(f, movie_id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        try:
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            if new_title:
                movie.title = new_title

            if new_release_date:
                movie.release_date = new_release_date

            movie.update()

            return jsonify({
                "success": True,
                "movies": movie.format()
            }), 200
        except:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(f, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted": movie_id
            }), 200
        except:
            abort(400)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()

        if not actors:
            abort(404)

        actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": actors
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(f):
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
            actor.insert()
            return jsonify({
                "success": True,
                "actors": actor.format()
            }), 200
        except:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(f, actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        try:
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)
            new_movie_id = body.get('movie_id', None)

            if new_name:
                actor.name = new_name
            if new_age:
                actor.age = new_age
            if new_gender:
                actor.gender = new_gender
            if new_movie_id:
                actor.movie_id = new_movie_id

            actor.update()

            return jsonify({
                "success": True,
                "actors": actor.format()
            }), 200
        except:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(f, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted": actor_id
            }), 200
        except:
            abort(400)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(port=8080, debug=True)
