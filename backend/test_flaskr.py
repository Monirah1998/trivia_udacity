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
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is name of program ?',
            'answer': 'Visual Studio',
            'category': '1',
            'difficulty': 5,
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # --------------- test case for success ---------------

# retrieve all categories

    def test_retrive_categories(self):
        res = self.client().get('/categories')
        
        self.assertEqual(res.status_code, 200)
   

# retrieve questions

    def test_retrieve_questions(self):
        
        res = self.client().get('/questions')
        
        self.assertEqual(res.status_code, 200)
    
    
    def test_retrieve_questions_for_category(self):
        
        res = self.client().get('/categories/1/questions')
     
        self.assertEqual(res.status_code, 200)
   

# add question

    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'What is your name ?',
            'answer': 'Monirah',
            'category': '4',
            'difficulty': 5,
        })
        
        self.assertEqual(res.status_code, 200)
      

# remove

    def test_remove_questions(self):
        res = self.client().delete('/questions/3')
        self.assertEqual(res.status_code, 200)
     

# search

    def search_question(self):
        search_key = {"searchTerm": "title"}
        res = self.client().post('questions/search', json=search_key)
        self.assertEqual(res.status_code, 200)

# quize

    def test_play_quiz(self):
        data = {
            'previous_questions': [2, 6],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', json=data)
        self.assertEqual(res.status_code, 200)
      

    # --------------- test case for failure ---------------

# page number

    def test_invalid_pages(self):
        res = self.client().get('/questions?page=10000')
        self.assertEqual(res.status_code, 404)
      

# search

    def test_invalid_search_input(self):
        res = self.client().post('/questions/search',
                                 json={"searchTerm": "kimikkjhgghn"})
        self.assertEqual(res.status_code, 404)
 

# add question

    def test_invalid_create_question(self):
        bad_question = {
            'question': 'why you join Full stack development?',
            'category': '1',
            'answer': '',
            'difficulty': 1,
        }
        res = self.client().post('/questions', json=bad_question)
        
        self.assertEqual(res.status_code, 422)
    

# category

    def test_not_found_category(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 422)
   

# quiz

    def test_quiz_fails(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [2, 6],
            'quiz_category': {
                'type': 'M',
                'id': 'X'
            
            }
        })
        self.assertEqual(res.status_code, 422)
     


    def test_remove_questions_failurs(self):
        res = self.client().delete('/questions/999')
        self.assertEqual(res.status_code, 422)
       

    def test_get_question_not_found(self):
        res = self.client().get('/questions/1000')
        self.assertEqual(res.status_code, 404)
  

    def test_get_category_not_found(self):
        res = self.client().get('/categories/19')
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
