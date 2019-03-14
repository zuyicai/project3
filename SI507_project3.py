### All set up

import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_movies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy


### Models

# Set up association Table between artists and albums
collections = db.Table('collections',db.Column('Director_id',db.Integer, db.ForeignKey('Director.id')),db.Column('Distributor_id',db.Integer, db.ForeignKey('Distributor.id')))

class movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    Distributor = db.Column(db.String(64), db.ForeignKey("Distributor.name")) #ok to be null for now
    Director = db.Column(db.String(64), db.ForeignKey("Director.name")) # ok to be null for now
    # distributor_id = db.Column(db.Integer, db.ForeignKey("Distributor.id")) #ok to be null for now
    # director_id = db.Column(db.Integer, db.ForeignKey("Director.id")) # ok to be null for now

    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.Director, self.Distributor)

class Rating(db.Model):
    __tablename__ = "Ratings"
    id = db.Column(db.Integer, primary_key=True)
    # movie = db.relationship('movie',backref='Rating')
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    MPAA_Rating = db.Column(db.REAL)
    Rotten_Tomatoes = db.Column(db.REAL)
    IMDB_Rating = db.Column(db.REAL)
    IMDB_Votes = db.Column(db.REAL)


class Distributor(db.Model):
    __tablename__ = "Distributor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # movie = db.relationship('movie',backref='Distributor')
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    location = db.Column(db.String(64))

    def __repr__(self):
        return "{} (Location: {})".format(self.name,self.location)


class Director(db.Model):
    __tablename__ = "Director"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # movie = db.relationship('movie',backref='Director')
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    Birth = db.Column(db.String(64))
    Nationality = db.Column(db.String(64))
    Party = db.Column(db.String(64))

    def __repr__(self):
        return "{} by {} | {}".format(self.movie,self.name, self.Nationality)


##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director





#### Set up Controllers (route functions) #####

## Main route
@app.route('/') # http://127.0.0.1:5000/
def index():
    movies = movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/Movie/new/<title>/<director>/<distributor>/') # http://127.0.0.1:5000/Movie/new/moonriver/Jack/DreamCo/
def new_movie(title, director, distributor):
    if movie.query.filter_by(title=title).first(): # if there is a song by that title
        return "That movie already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        newmo = movie(title=title, Director=director.name,Distributor=distributor)
        session.add(newmo)
        session.commit()
        return "New movie: {} by {}. Check out the URL for ALL movies to see the whole list.".format(newmo.title, director.name)


@app.route('/all_movies') # http://127.0.0.1:5000/all_movies
def see_all():
    all_movies = [] # Will be be tuple list of title, director, distributor
    movies = movie.query.all()
    for mo in movies:
        director = Director.query.filter_by(name=mo.Director).first() # get just one artist instance
        all_movies.append((mo.title,director.name, mo.Distributor)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors')
def see_all_directors():
    directors = Director.query.all()
    names = []
    for dir in directors:
        num_movies = len(movie.query.filter_by(Director=dir.name).all())
        newtup = (dir.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_directors.html',director_names=names)


if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
