import os
from flask import Flask, jsonify, request, abort
from database.models import setup_db
from flask_cors import CORS
from database.models import Actor, Movie, Cast
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins.
    """
    cors = CORS(app,
                resources={r"*": {"origins": "*"}},
                supports_credentials=True)

    """
    Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )

        return response

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + ("!!!!! You are doing great "
                                   "in this Udacity project.")
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    """
    Actors
    """

    @app.route('/api/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(payload):
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.short() for actor in actors]
        })

    @app.route('/api/actors', methods=['POST'])
    @requires_auth("post:actors")
    def add_actor(payload):
        request_data = request.get_json()
        try:
            actor = Actor(request_data['name'],
                          request_data['age'],
                          request_data['gender'])
            actor.insert()
        except Exception as e:
            print(e)
            abort(400)

        return jsonify({
            'success': True,
            'actor': actor.short()
        })

    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        request_data = request.get_json()
        actor = Actor.query.get_or_404(id)

        try:
            if 'name' in request_data:
                actor.name = request_data['name']
            if 'age' in request_data:
                actor.age = request_data['age']
            if 'gender' in request_data:
                actor.gender = request_data['gender']
            actor.update()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'actor': actor.short()
        })

    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.get_or_404(id)
        try:
            actor.delete()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'actor': actor.short()
        })

    """
    Movies
    """

    @app.route('/api/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(payload):
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.short() for movie in movies]
        })

    @app.route('/api/movies', methods=['POST'])
    @requires_auth("post:movies")
    def add_movies(payload):
        request_data = request.get_json()
        try:
            movie = Movie(request_data['title'], request_data['release_date'])
            movie.insert()
        except Exception as e:
            print(e)
            abort(400)

        return jsonify({
            'success': True,
            'movie': movie.short()
        })

    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        request_data = request.get_json()
        movie = Movie.query.get_or_404(id)

        try:
            if 'title' in request_data:
                movie.title = request_data['title']
            if 'release_date' in request_data:
                movie.release_date = request_data['release_date']
            movie.update()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'movie': movie.short()
        })

    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.get_or_404(id)
        try:
            movie.delete()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'movie': movie.short()
        })

    """
    Casts
    """

    @app.route('/api/casts', methods=['GET'])
    def get_all_casts():
        casts = Cast.query.all()

        return jsonify({
            'success': True,
            'casts': [cast.format() for cast in casts]
        })

    @app.route('/api/casts', methods=['POST'])
    def create_cast():
        request_data = request.get_json()
        try:
            cast = Cast(request_data['movie_id'], request_data['actor_id'])
            cast.insert()
        except Exception as e:
            print(e)
            abort(400)

        return jsonify({
            'success': True,
            'cast': cast.format()
        })

    @app.route('/api/casts/<int:id>', methods=['PATCH'])
    def update_cast(payload, id):
        request_data = request.get_json()
        cast = Cast.query.get_or_404(id)
        try:
            cast.movie_id = request_data['movie_id']
            cast.actor_id = request_data['actor_id']
            cast.update()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'cast': cast.format()
        })

    @app.route('/api/casts/<int:id>', methods=['DELETE'])
    def delete_cast(payload, id):
        cast = Cast.query.get_or_404(id)
        try:
            cast.delete()
        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'cast': cast.format()
        })

    """
    Error handling
    """

    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
