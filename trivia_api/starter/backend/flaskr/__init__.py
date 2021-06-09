import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10




def paginate_question(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Credentials', 'true')
      response.headers.add(
          'Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
          
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def get_categories():

      dict_category = {}
      category = Category.query.order_by(Category.id).all()
      
      for cat in category:
          dict_category[cat.id] = cat.type

      return jsonify({ 'categories': dict_category })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def get_questions():
      try:
          questions = Question.query.order_by(Question.id).all()
          formatted_questions = [q.format() for q in questions]
          current_questions = paginate_question(request, questions)

          dict_category = {}
          category = Category.query.order_by(Category.id).all()
      
          for cat in category:
              dict_category[cat.id] = cat.type
          if len(current_questions) == 0:
              abort(400)

          curr_categs = list(set([q['category'] for q in current_questions]))
          current_category = curr_categs
          return jsonify({
              'questions': current_questions,
              'total_questions': len(questions),
              'current_category': current_category,
              'categories': dict_category,
              'success': True
          })
      except BaseException:
          abort(404)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def delete_question(question_id):
      selected_question = Question.query.get(question_id)

      if selected_question is None:
          abort(404)
      try:
          selected_question.delete()

          return jsonify ({
                
                'success': True ,
                'deleted' : question_id 
            })
      except BaseException:
          abort(400)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def add_questions():
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)
      try:
          new_question = Question(
              question=new_question,
              answer=new_answer,
              difficulty=new_difficulty,
              category=new_category)
          new_question.insert()
          return jsonify({
              'success': True
          })
      except BaseException:
          abort(400)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search_questions', methods=['POST'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def search_questions():
      body = request.get_json()
      term = body.get('searchTerm')
      if term is None:
          abort(404)

      try:
          select_terms = Question.query.filter(Question.question.ilike('%{}%'.format(term))).all()
          result = paginate_question(request, select_terms)

          if(len(result) == 0):
              
              abort(404)
          print(result)
          return jsonify({
              'success': True,
              'questions': result,
              'totalQuestions': len(result),
              'currentCategory': None
          })
      except BaseException:
          abort(404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def questions_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=category_id).all()
            current_questions = paginate_question(request, questions)


            categories = Category.query.all()
            for cat in categories:
                formatted_categories = cat.format()
             
            
            for question in current_questions:
                current_categories = list(set([question['category']]))
                
            current_category = current_categories

            if category_id > 6:
                abort(404)

            return jsonify({
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': current_category,
                'categories': formatted_categories,
                'success': True
            })
        except BaseException:
            abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
  def quizzes():
      if request.method == 'POST':
          responce = request.get_json()
          catagory = responce.get('quiz_category',None).get('id')

          if catagory != 0:
                questions = Question.query.filter(
                Question.catagory == catagory).all()
          else:
                questions = Question.query.all()
           
          if len(questions) > 0:
              prev_questions = responce.get('previous_questions', None)
              for question in questions:
                  if question.id not in prev_questions:
                        subquastions = question.format()
                  
              Noumber_subquastions = len(subquastions)
              Noumber_prev_questions = len(prev_questions)

          else:
              return jsonify({
                'question': None
            })

          if Noumber_subquastions > 0:
               question = random.choice(subquastions)
          else:
              question = None

          try:
              while Noumber_subquastions > Noumber_prev_questions:
                  if question.get(id) not in prev_questions:
                       return jsonify({
                        'success': True,
                        'question': question
                    }), 200
              return jsonify({
                'success': True,
                'question': question
            }), 200
          except BaseException:
            abort(404)
      else:
          abort(404)










  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def Error400(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request ,Something went wrong try again later'
    }), 400

  @app.errorhandler(401)
  def Error401(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized , Try again later'
    }), 401

  @app.errorhandler(404)
  def Error404(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Sorry question was not found'
    }), 404

  @app.errorhandler(405)
  def Error405(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Sorry this method is Not Allowed'
    }), 405

  @app.errorhandler(422)
  def Error422(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity, Try again.'
    }), 422

  @app.errorhandler(500)
  def Error500(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error,Try again later'
    }), 500

  
  return app

    