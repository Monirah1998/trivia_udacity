import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    question = [question.format() for question in selection]
    current_questions = question[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def categories():
        try:
            categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in categories]
            return jsonify({
                'success': True,
                'categories': formatted_categories

            })
        except:
            abort(404)

    @app.route('/questions')
    def questions():
        try:
            # all questions
            query_ques = Question.query.all()
            # total questions
            total = len(query_ques)
            # 10 questions
            questions_10 = paginate_questions(request, query_ques)
            # current category
            # categories
            categoriesQuery = Category.query.all()
            categories_type = {}
            for category in categoriesQuery:
                categories_type[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': questions_10,
                'total_questions': total,
                'categories': categories_type,
                'current_category': None
            })
        except:
            abort(404)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )
        except Exception as e:

            abort(422)

    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()

        NewQuestion = body.get('question', None)
        answerQuestion = body.get('answer', None)
        categoryQuestion = body.get('category', None)
        difficultyScore = body.get('difficulty', None)
        try:
            AddQuestion = Question(question=NewQuestion, answer=answerQuestion,
                                   category=categoryQuestion, difficulty=difficultyScore)
            AddQuestion.insert()
            return jsonify(
                {
                    "success": True,
                    "created": AddQuestion.id
                }
            )
        except Exception as e:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        searchfunction = body.get('searchTerm')

        results = Question.query.filter(
            Question.question.ilike(f'%{searchfunction}%')).all()
        questions = [question.format() for question in results]

        return jsonify({
            'success': True,
            'questions': questions
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_basedon_category(category_id):
        categoryID = str(category_id)
        questions = Question.query.filter(
            Question.category == categoryID).all()
        paginated = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': paginated
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        try:
            body = request.get_json()
            previousques = body.get('previous_questions', None)
            quizCategory = body.get('quiz_category', None)
            categorytype = quizCategory['id']

            if categorytype == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previousques)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(
                    previousques), Question.category == categorytype).all()

            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except:
            abort(422)

# --------------------- ERROR HANDLER --------------------

    app.errorhandler(404)

    def notfound(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    app.errorhandler(422)

    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    app.errorhandler(400)

    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    return app
