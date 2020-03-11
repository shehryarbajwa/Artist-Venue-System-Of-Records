## Fyyur
Fyyur is a Udacity Fullstack Nanodegree project which facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Tech Stack

SQLAlchemy ORM to be our ORM library of choice
PostgreSQL as our database of choice
Python3 and Flask as our server language and server framework
Flask-Migrate for creating and running schema migrations
HTML, CSS, and Javascript with Bootstrap 3 for our website's frontend
Development Setup
First, install Flask if you haven't already.

$ cd ~
$ sudo pip3 install Flask
To start and run the local development server,

## Live Demo

https://fyyur-sbajwa.herokuapp.com/

## Lessons Learnt

Created the front end in Jinja2 and the backend in Flask and PostgreSQL. 
use the SQLAlchemy ORM to create the database and complete the database migrations. Learnt the use of forms and form validation with WFForms and Validator logic. Finally deployed the full stack application to Heroku


## Install the dependencies:
$ pip install -r requirements.txt
Run the development server:
$ export FLASK_APP=app.py
$ export FLASK_ENV=development # enables debug mode
$ python3 app.py
Navigate to Home page http://localhost:5000