import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        results = [drink.short() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": results
        }), 200
    except:
        abort(404)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(f):
    drinks = Drink.query.all()
    try:
        results = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": results
        }), 200
    except:
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(f):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title == None or recipe == None:
        abort(422)

    try:
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except:
        abort(400)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(f, drink_id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        request_title = body.get('title', None)
        request_recipe = body.get('recipe', None)

        if request_title:
            drink.title = request_title

        if request_recipe:
            drink.recipe = json.dumps(body['recipe'])

        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except:
        abort(400)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(f, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)
    try:
        drink.delete()
        return jsonify(
            {"success": True, "delete": drink_id}
        )
    except:
        abort(400)

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
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
        'error': 401,
        'message': 'Unauthorized'
    }), 401
