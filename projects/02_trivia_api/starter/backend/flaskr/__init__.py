import os
import sys

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def format_categories(categories):
    formatted = {}
    for category in categories:
        formatted[category.id] = category.type
    return formatted


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        return jsonify({
            "categories": format_categories(selection),
            "success": True
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        if len(search_term := request.args.get('search', '')) > 0:
            return search_questions(search_term)
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, all_questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'total_questions': len(all_questions),
            'questions': current_questions,
            'categories': format_categories(Category.query.order_by(Category.id).all()),
            # 'current_category': Category.query.all()[0].format(),
            'success': True
        })

    def search_questions(search_term):
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        paged = paginate_questions(request, questions)

        if len(paged) == 0 and len(questions) != 0:
            # If matching questions exist, but not within that page, we have a bad page
            abort(404)

        return jsonify({
            "questions": paged,
            "total_questions": len(questions),
            "success": True
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question.id
            })
        except Exception as e:
            if e.code == 404:
                abort(404)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        question = data.get('question', '')
        answer = data.get('answer', '')
        difficulty = data.get('difficulty', 1)
        category = data.get('category', None)
        if category is None:
            abort(400)
        try:
            if len(question) < 1 or len(answer) < 1:
                abort(400)
            category = Category.query.filter(Category.id == category).one_or_none()
            if category is None:
                abort(404)
            difficulty = int(difficulty)
            if difficulty < 1 or difficulty > 5:
                abort(400)
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category.id
            )
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id
            }), 201
        except Exception as e:
            if e.code == 400:
                abort(400)
            if e.code == 404:
                abort(404)
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        matching_questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, matching_questions)

        if len(current_questions) == 0 and len(matching_questions) != 0:
            abort(404)

        return jsonify({
            'total_questions': len(matching_questions),
            'questions': current_questions,
            'success': True,
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def play_game():
        data = request.get_json()
        category_id = data['quiz_category']
        previous = data['previous_questions']

        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None and category_id != 0:
            abort(400)

        query = Question.query.filter(Question.id.notin_(previous))
        if category_id != 0:
            query = query.filter(Question.category == category_id)
        matching_questions = query.all()

        question = None
        if len(matching_questions) > 0:
            question = random.choice(matching_questions).format()

        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    return app
