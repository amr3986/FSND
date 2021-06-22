Udacity - Full Stack Trivia App

This app is simple game that aim to test your knowledge in different catagory also it allow you to add your own question, lets the fun beggin

Trivia features:
1-Add questions and answer in any catagory.
2-Delete unwanted questions easly.
3-Display questions with the ability to filter by catagory.
4-Questions page should show the question, category and difficulty rating by default and can show/hide the answer.
5-Play the quiz game, where the quastions appear in random way.
6-Search for questions using text from the quastion itself.


To run this project successfully we recommend following the instructions:

./frontend/
./backend/

Backend
The ./backend directory contains a completed Flask and SQLAlchemy server. You will work primarily in __init__.py which contain endpoints and can reference models.py for DB and SQLAlchemy setup.

Installing Dependencies for ./backend:

1-Installing from requiremnts.txt file run:
pip install -R requiremnts.txt

Running Your Backend

1- navigate to ./backend directory and run:
export FLASK_APP=flaskr
flask run --port=5000

Frontend
The ./frontend directory contains a complete React frontend to consume the data from the Flask server.

Installing Dependencies for ./frontend:

1-Installing Node and NPM
download and install Node from https://nodejs.com/en/download.

2-Installing project dependencies run:

npm install

Running Your Frontend

1- navigate to ./frontend directory and run:
npm start 
