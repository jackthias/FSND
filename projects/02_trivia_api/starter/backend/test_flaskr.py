import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_categories_wrong_method(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertTrue(data['message'])

    def test_get_question_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

    def test_get_question_missing_page(self):
        res = self.client().get('/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_delete_question_success(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['deleted'], int)

        res2 = self.client().get('/questions')
        data2 = json.loads(res2.data)
        qs = [q['id'] for q in data2['questions']]
        self.assertNotIn(2, qs)

    def test_delete_question_missing(self):
        res = self.client().delete('/questions/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_create_question_success(self):
        attributes = {
            'question': "Test question",
            'answer': "Test answer",
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=attributes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        created = data['created']
        self.assertIsInstance(created, int)

        q = Question.query.get(created)
        self.assertEqual(q.id, created)
        self.assertEqual(q.question, attributes['question'])
        self.assertEqual(q.answer, attributes['answer'])
        self.assertEqual(q.difficulty, attributes['difficulty'])

    def test_create_question_bad_difficulty(self):
        attributes = {
            'question': "Test question",
            'answer': "Test answer",
            'difficulty': 6,
            'category': 1
        }
        res = self.client().post('/questions', json=attributes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])

    def test_create_question_no_question(self):
        attributes = {
            'answer': "Test answer",
            'difficulty': 3,
            'category': 1
        }
        res = self.client().post('/questions', json=attributes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])

    def test_create_question_no_answer(self):
        attributes = {
            'question': "Test question",
            'difficulty': 3,
            'category': 1
        }
        res = self.client().post('/questions', json=attributes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])

    def test_create_question_bad_category(self):
        attributes = {
            'question': "Test question",
            'answer': "Test answer",
            'difficulty': 3,
            'category': 99999
        }
        res = self.client().post('/questions', json=attributes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_search_questions_success(self):
        res = self.client().get('/questions?search=country')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

    def test_search_questions_success_paged(self):
        res = self.client().get('/questions?search=country&page1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

    def test_search_questions_bad_page(self):
        res = self.client().get('/questions?search=country&page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_get_question_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['total_questions'], int)

        self.assertListEqual([q['category'] for q in data['questions']], [1] * len(data['questions']))

    def test_get_question_by_category_bad_page(self):
        res = self.client().get('/categories/1/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_play_quiz_success(self):
        prev = []
        res = self.client().post('/quizzes', json={
            'quiz_category': 5,
            'previous_questions': prev
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        q = data['question']
        self.assertTrue(q)
        prev.append(q['id'])

        res = self.client().post('/quizzes', json={
            'quiz_category': 5,
            'previous_questions': prev
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        q = data['question']
        self.assertTrue(q)
        prev.append(q['id'])

        res = self.client().post('/quizzes', json={
            'quiz_category': 5,
            'previous_questions': prev
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(data.get('question', None))

    def test_play_quiz_bad_category(self):
        res = self.client().post('/quizzes', json={
            'quiz_category': 9999,
            'previous_questions': []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()