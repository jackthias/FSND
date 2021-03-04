# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Documentation

### Introduction

This API provides the backend for this trivia application, interfacing with
the database to provide common requests to the frontend. This is a RESTful
API.

### Getting Started

The base URL for this API is `http://127.0.0.1:5000/`

Requests are made in the form `http://127.0.0.1:5000/<endpoint>`.
You can check the [Endpoint Library](#Endpoint-Library) for a comprehensive
list of available endpoints.

There is no authentication for this API.

### Errors

Errors should only be returned with the following
code:
* 400
* 404
* 405
* 422

Error responses should include a JSON body in the
following form:
```json
{
    "success": False,
    "error": 422,
    "message": "Unprocessable entity"
}
```

### Endpoint Library

#### `GET '/categories'`

Returns a list of all categories.

##### Example:

Request:

`curl --location --request GET 'http://127.0.0.1:5000/categories'`

Response:

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

Status: 200

#### `GET '/questions'`

Returns a paginated list of questions, along with the
count of all questions.

Optional argument `int:page` specifies which page
of questions should be retrieved. 

##### Example:

Request:

`curl --location --request GET 'http://127.0.0.1:5000/questions'`

Response:

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 15
}
```
Status: 200

Request:

`curl --location --request GET 'http://127.0.0.1:5000/questions?page=2'`

Response:

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "Test 1"
        }
    ],
    "success": true,
    "total_questions": 14
}
```

#### `GET '/questions?search<term>'`

Gets a paginated list of all results with questions
that contain the search term provided with the argument:
`search`.

Optional argument `page` can be used to select another
page if there is more than one page of results.

##### Examples:

Request:

`curl --location --request GET 'http://127.0.0.1:5000/questions?search=test'`

Response:

```json
{
    "questions": [
        {
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "Test 1"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

Status: 200

#### `DELETE '/questions/<int:question_id>'`

Deletes the question with the id matching the uri index.

**CAUTION: This is a destructive operation.**

##### Example:

Request:

`curl --location --request DELETE 'http://127.0.0.1:5000/questions/4'`

Response:

```json
{
    "deleted": 4,
    "success": true
}
```

Status: 200

#### `POST /questions`

Creates a new question based on the provided JSON body.

##### Example:

Request:

```curl
curl --location --request POST 'http://127.0.0.1:5000/questions' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "Test",
    "answer": "Test",
    "difficulty": 1,
    "category": 1
}'
```

Response:

```json
{
    "created": 28,
    "success": true
}
```

Status: 201

#### `GET '/categories/<int:category_id>/questions'`

Gets a paginated list of the questions belonging the category
provided in the URI index.

##### Example:

Request:

`curl --location --request GET 'http://127.0.0.1:5000/categories/1/questions'`

Response:

```json
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "Test 1"
        },
        {
            "answer": "Test",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": "Test"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

Status: 200 

#### `POST '/quizzes'`

Returns a random question.

The parameter `"quiz_category"` can be used to specify a
category to grab questions from. `0` specifies all categories.

The parameter `""previous_questions"` can be used to specify a
list of questions that shouldn't be grabbed.

If there are no questions grabbed, the request will still
a 200 status code. This can be used to indicate that the quiz is
over.

##### Examples:

Request:

```curl
curl --location --request POST 'http://127.0.0.1:5000/quizzes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "quiz_category": 0,
    "previous_questions": []
}'
```

Response:

```json
{
    "question": {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    "success": true
}
```

Status: 200

Request:

```curl
curl --location --request POST 'http://127.0.0.1:5000/quizzes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "quiz_category": 5,
    "previous_questions": []
}'
```

Response:

```json
{
    "question": {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    "success": true
}
```

Status: 200

Request:

```curl
curl --location --request POST 'http://127.0.0.1:5000/quizzes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "quiz_category": 5,
    "previous_questions": [6]
}'
```

Response:

```json
{
    "question": null,
    "success": true
}
```

Status: 200

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```