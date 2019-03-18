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

# Set up association Table between distributors and directors: many to many. In this database, I didn't write this relationship.
collections = db.Table('collections',
    db.Column('Director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True),
    db.Column('Distributor_id', db.Integer, db.ForeignKey('distributor.id'), primary_key=True))


class Distributor(db.Model):
    __tablename__ = "distributor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    location = db.Column(db.String(64))
    movies = db.relationship("movie",backref="Distributor") # Distributor-movie:one to many
    directors = db.relationship('Director', secondary=collections, lazy='subquery', backref=db.backref('Distributor', lazy=True))


    def __repr__(self):
        return "{} (Location: {})".format(self.name,self.location)


class Director(db.Model):
    __tablename__ = "director"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    Birth = db.Column(db.String(64))
    Nationality = db.Column(db.String(64))
    Party = db.Column(db.String(64))
    movies = db.relationship("movie",backref="Director") # Director-movie:one to many

    def __repr__(self):
        return "{}'s personal information: Birth: {}, Nationality:{}, Party:{}.".format(self.name,self.Birth, self.Nationality,self.Party)


class Rating(db.Model):
    __tablename__ = "Ratings"
    id = db.Column(db.Integer, primary_key=True)
    moname = db.Column(db.String(64),unique=True)
    movie = db.relationship("movie", backref=db.backref("Ratings", uselist=False))# movie-rating: one to one
    MPAA_Rating = db.Column(db.REAL)
    Rotten_Tomatoes = db.Column(db.REAL)
    IMDB_Rating = db.Column(db.REAL)
    IMDB_Votes = db.Column(db.REAL)

    def __repr__(self):
        return"{} has ratings: MPAA_Rating {}, Rotten_Tomatoes {}, IMDB_Rating {}, IMDB_Votes {}.".format(self.moname,self.MPAA_Rating,self.Rotten_Tomatoes,self.IMDB_Rating,self.IMDB_Votes)


class movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    # Rating_id = db.Column(db.REAL, db.ForeignKey("Ratings.id")) # !!! ForeignKey should only be the id- primary_key
    Distributor_id = db.Column(db.Integer, db.ForeignKey("distributor.id")) #ok to be null for now
    Director_id = db.Column(db.Integer, db.ForeignKey("director.id")) # ok to be null for now
    rating_id = db.Column(db.Integer, db.ForeignKey("Ratings.id"))

    # ratings = db.relationship("Rating",backref="movie")



    def __repr__(self):
        return "{} by director {} |  Distributor {}. {} has ratings information, please refer to {}".format(self.title,self.Director_id, self.Distributor_id, self.title, self.rating_id)




##### Helper functions #####

### For database additions
### Relying on global session variable above existing


# get or create director
def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

# get or create distributor
def get_or_create_distibutor(distributor_name):
    distributor = Distributor.query.filter_by(name=distributor_name).first()
    if distributor:
        return distributor
    else:
        distributor = Distributor(name=distributor_name)
        session.add(distributor)
        session.commit()
        return distributor

# get or create rating, here I only create Rotten_Tomatoes rating because it's much typical and we don't need to list all ratings when creating the movieself.
# We will have detailed ratings information by special route to create and add ratings to certain movie.
def get_or_create_rating(movie_title,rating_Rotten):
    rating = Rating.query.filter_by(moname = movie_title).first()
    if rating:
        return rating
    else:
        rating = Rating(moname = movie_title, Rotten_Tomatoes=rating_Rotten)
        session.add(rating)
        session.commit()
        return rating





#### Set up Controllers (route functions) #####

## Main route
# This route is a basic route to welcome readers~ And it shows the number of movies already existed in this database.
@app.route('/') # http://127.0.0.1:5000/
def index():
    movies = movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/Movie/new/<title>/<director>/<distributor>/<rating>') # http://127.0.0.1:5000/Movie/new/moonriver/Jack/DreamCo/8.0
def new_movie(title, director, distributor, rating):
    if movie.query.filter_by(title=title).first():# if there is a movie by that title
       return "That movie already exists! Go back to the home page!"
    else: # If not, we will create this movie and add it to our database
       director = get_or_create_director(director)
       distributor = get_or_create_distibutor(distributor)
       rating = get_or_create_rating(title,rating)
       newmo = movie(title=title, Director_id = director.id, Distributor_id = distributor.id, rating_id = rating.id)
       session.add(newmo)
       session.commit()
       return render_template('new_movie.html',new_movie = newmo.title,new_director = newmo.Director_id,new_distributor = newmo.Distributor_id,new_rating = newmo.rating_id)
        # return "New movie: {} by {}. Check out the URL for ALL movies to see the whole list.".format(newmo.title, director.name)


@app.route('/all_movies') # http://127.0.0.1:5000/all_movies
def see_all():
    all_movies = [] # Will be be tuple list of title, director, distributor
    movies = movie.query.all()
    for mo in movies:
        director = Director.query.filter_by(id=mo.Director_id).first() # get just one artist instance
        distributor_name = Distributor.query.filter_by(id=mo.Distributor_id).first()
        all_movies.append((mo.title,director.name, distributor_name.name)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors') # http://127.0.0.1:5000/all_directors
def see_all_directors():
    directors = Director.query.all()
    names = []
    for dir in directors:
        num_movies = len(movie.query.filter_by(Director_id=dir.id).all())
        newtup = (dir.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_directors.html',director_names=names)

@app.route('/all_distributors') #http://127.0.0.1:5000/all_distributors
def see_all_distributor():
    distributors = Distributor.query.all()
    names = []
    for dis in distributors:
        num_movies = len(movie.query.filter_by(Distributor_id=dis.id).all())
        newtup = (dis.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_distributors.html',distributor_names=names)

# This route is for inputting ratings info.
@app.route('/<movie_title>/<rating_MPAA>/<rating_Rotten>/<rating_IMDB_R>/<rating_IMDB_V>') # http://127.0.0.1:5000/moonriver/7/8/9/7.7
def see_all_ratings(movie_title, rating_MPAA, rating_Rotten, rating_IMDB_R, rating_IMDB_V):
    if movie.query.filter_by(title = movie_title).first():
        themovie = Rating.query.filter_by(moname = movie_title, Rotten_Tomatoes = rating_Rotten).first()
        themovie.MPAA_Rating = rating_MPAA
        themovie.Rotten_Tomatoes = rating_Rotten
        themovie.IMDB_Rating = rating_IMDB_R
        themovie.IMDB_Votes = rating_IMDB_V
        # rating = Rating(moname = movie_title, MPAA_Rating = rating_MPAA, Rotten_Tomatoes = rating_Rotten, IMDB_Rating = rating_IMDB_R,IMDB_Votes = rating_IMDB_V)
        session.add(themovie)
        session.commit()
        return "That movie {} has ratings! MPAA_Rating:{}. Rotten_Tomatoes:{}. IMDB_Rating:{}. IMDB_Votes:{}.".format(movie_title, themovie.MPAA_Rating,themovie.Rotten_Tomatoes,themovie.IMDB_Rating,themovie.IMDB_Votes)
    else:
        return "That movie doesn't have record. Please input the information and then to check."

# This route is for inputting directors info.
@app.route('/Director/<director>/<birth>/<nationality>/<party>') # http://127.0.0.1:5000/Director/Jack/1972.10.09/theUS/USparty
def see_directors(director,birth,nationality,party):
    if Director.query.filter_by(name = director).first():
        thedir = Director.query.filter_by(name = director).first()
        thedir.Birth = birth
        thedir.Nationality = nationality
        thedir.Party = party
        session.add(thedir)
        session.commit()
        names = []
        movie_list = movie.query.filter_by(Director_id = thedir.id).all()
        num_movies = len(movie_list)
        newtup = (thedir.name,num_movies,movie_list)
        names.append(newtup)
        return render_template('all_directors.html',director_names=names)
    else:
        return "That director doesn't have record. Please input the information and then to check."


# This route is for inputting distributors info.
@app.route('/Distributor/<distributor>/<location>') # http://127.0.0.1:5000/Distributor/DreamCo/Los%20Angeles
def see_distributors(distributor,location):
    if Distributor.query.filter_by(name = distributor).first():
        thedis = Distributor.query.filter_by(name = distributor).first()
        thedis.location = location
        session.add(thedis)
        session.commit()
        names = []
        movie_list = movie.query.filter_by(Distributor_id = thedis.id).all()
        num_movies = len(movie_list)
        newtup = (thedis.name,num_movies,movie_list)
        names.append(newtup)
        return render_template('all_distributors.html',distributor_names=names)
    else:
        return "That distributor doesn't have record. Please input the information and then to check."



if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python SI507_project3.py runserver
