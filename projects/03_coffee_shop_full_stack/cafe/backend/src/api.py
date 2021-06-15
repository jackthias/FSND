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

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()

# Utilities


def fetch_drinks(long=False, drink_id=None):
    q = Drink.query
    if drink_id is not None:
        q = q.filter(Drink.id == drink_id)
    if long:
        return [drink.long() for drink in q.all()]
    return [drink.short() for drink in q.all()]


# ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    :return: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    return jsonify({
        "success": True,
        "drinks": fetch_drinks()
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details():
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation

    :return: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    return jsonify({
        "success": True,
        "drinks": fetch_drinks(long=True)
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation

    :return: status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly
    created drink or appropriate status code indicating reason for failure
    """
    data = request.get_json()
    title = data.get('title', '')
    recipe_obj = data.get('recipe', {})
    recipe = json.dumps(recipe_obj)
    try:
        if len(title) < 1:
            abort(400, '"title" is a required field in request body.')
        if len(recipe_obj) < 1:
            abort(400, '"recipe" is a required field in request body.')
        validate_recipe(recipe_obj)
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
    except Exception as e:
        if e.code in [400]:
            abort(e.code, e.description)
        abort(422)
    return jsonify({
        "success": True,
        "drinks": fetch_drinks(long=True)
    })


recipe_params = ('name', 'color', 'parts')


def validate_recipe(recipe):
    if not isinstance(recipe, list):
        abort(400, "Recipe must be a list of objects.")
    for item in recipe:
        if not isinstance(item, dict):
            abort(400, "Recipe must be a list of objects.")
        if not all(key in item for key in recipe_params):
            abort(400, f"Recipe objects require {recipe_params}")
        if not isinstance(item['name'], str):
            abort(400, "Name of ingredient in recipe must be a string.")
        if not isinstance(item['color'], str):
            abort(400, "Color of ingredient in recipe must be a string.")
        if not isinstance(item['parts'], int):
            abort(400, "Parts of ingredient in recipe must be an integer.")


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    """
    PATCH /drinks/<drink_id>
        where <drink_id> is the existing model id
        it should respond with a 404 error if <drink_id> is not found
        it should update the corresponding row for <drink_id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation

    :param drink_id: is the existing model id
    :return: status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the
    updated drink or appropriate status code indicating reason for failure
    """
    data = request.get_json()
    if len(data) < 1:
        abort(400)
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)
        if 'title' in data:
            drink.title = data['title']
        if 'recipe' in data:
            recipe_candidate = data['recipe']
            validate_recipe(recipe_candidate)
            drink.recipe = json.dumps(recipe_candidate)
        drink.update()
    except Exception as e:
        if e.code in [400, 404]:
            abort(e.code, e.description)
        abort(422)
    return jsonify({
        'success': True,
        'drinks': fetch_drinks(long=True, drink_id=drink_id)
    })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    """
    DELETE /drinks/<drink_id>
        where <drink_id> is the existing model id
        it should respond with a 404 error if <drink_id> is not found
        it should delete the corresponding row for <drink_id>
        it should require the 'delete:drinks' permission

    :param drink_id: the existing model id
    :return: status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception as e:
        if e.code in [404]:
            abort(e.code, e.description)
        abort(422)


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    """
    error handling for unprocessable entity
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable",
        "details": get_error_description(error)
    }), 422


@app.errorhandler(400)
def bad_request(error):
    """
    error handling for bad request
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request",
        "details": get_error_description(error)
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    """
    error handling for method not allowed
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed",
        "details": get_error_description(error)
    }), 405


@app.errorhandler(404)
def not_found(error):
    """
    error handling for not found
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found",
        "details": get_error_description(error)
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    error handling for unauthorized
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized",
        "details": get_error_description(error)
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """
    error handling for forbidden
    :type error: Exception
    :param error: originating error
    :return: json error response
    """
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden",
        "details": get_error_description(error)
    }), 403


def get_error_description(error):
    return error.description if error.description else ""
