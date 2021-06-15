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


def fetch_drinks(long=False, id=None):
    q = Drink.query
    if id is not None:
        q = q.filter(Drink.id == id)
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
        if len(title) < 1 or len(recipe) < 1:
            abort(400)
        validate_recipe(recipe_obj)
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
    except Exception as e:
        if e.code == 400:
            abort(400)
        abort(422)
    return jsonify({
        "success": True,
        "drinks": fetch_drinks(long=True)
    })


recipe_params = ('name', 'color', 'parts')


def validate_recipe(recipe):
    if not isinstance(recipe, list):
        abort(400)
    for item in recipe:
        if not isinstance(item, dict):
            abort(400)
        if not all(key in item for key in recipe_params):
            abort(400)
        if not isinstance(item['name'], str):
            abort(400)
        if not isinstance(item['color'], str):
            abort(400)
        if not isinstance(item['parts'], int):
            abort(400)


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
        if e.code == 404:
            abort(404)
        if e.code == 400:
            abort(400)
        abort(422)
    return jsonify({
        'success': True,
        'drinks': fetch_drinks(long=True, id=drink_id)
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
