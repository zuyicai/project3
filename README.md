# Project3_zuyicai: A Simple Movie Flask App

This's a whole web application — a very simple one, using the web framework called Flask. Using this small application, you can get different outputs in the form of URLs. In this project, I created the database and added information to this database by using different URLs and different input.

SI507_project3.py is the file that I create the class and define the functional structure of this system, plus the routes; templates is the file that I create the htmls for different appearance of URLs. Here I referred to the diagram of the database that I created for project2. In this database, "Rating" to "movie" is one to one, "Director" to "movie" is many to one, "Distributor" to "movie" is many to one, "Distributor" to "Director" is many to many(Here I just show the relationship).

* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/plan.png)


Actually, I improve the app by adding serval routes such as all_distributors, all_directors and ratings, and this app has routes to add details to director and distributor. Thus readers can get the whole picture of the movie with the director, the distributor and different ratings.

Readers need to follow the steps to install everything needed to run this application.

## Getting Started

* Anaconda installed
* Open your terminal window! `cd` to the place where you want this project to go.
* This repository cloned to somewhere in your computer (the place).
```
git clone <git url>
```
* `cd` into where the project lives
* Create a virtual environment for it
```
virtualenv env
```
* Activate the virtual environment
```
$ source <projectname>-env/bin/activate    # For Mac/Linux...
$ source <projectname>-env/Scripts/activate    # For Windows
(project3-env) $     # you've succeeded if you see this after!
```
* install all requirement
```
pip install -r requirements.txt
```
```
Deactivate
```
* Just run the movie database app!
```
python SI507_project3.py runserver
```
* Check out what’s happening in your terminal window!
* Open a web browser, type in and check out this URL:
http://127.0.0.1:5000/
* you will see "number movies recorded". Here number will depend upon how many movies are already in your database.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/home.png)

* Open another tab and go to:
http://127.0.0.1:5000/Movie/new/moonriver/Jack/DreamCo/8.0(This is an example of a movie called moonriver with Rotten_Tomatoes rating 8.0, which is directed by Jack and distributed by DreamCo)
* After this you will see the following image. (Here the name of movie will depend on what you input in the URL:<title>, the director of movie will depend on what you input in the URL:<director>, the distributor of movie will depend on what you input in the URL:<distributor>.)
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/movie1.png)
* If we already have this movie in our database, it will shows the following information:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/movie2.png)
* This route is wrote with the use of "render_template". It's what we learned recently in class. And this one has to do with the html file in templates file.

* Now try going to:
http://127.0.0.1:5000/all_movies
* This route shows the list of all movies saved with the distributor and director.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/allm.png)


* Then:
http://127.0.0.1:5000/all_directors
* This route shows the list of all directors and the number of movies they directed.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/alldir.png)


* Then:
http://127.0.0.1:5000/all_distributors
* This route shows the list of all distributors and the number of movies they distributed.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/alldis.png)

* Then:
http://127.0.0.1:5000/moonriver/7/8/9/7.7
* This route is the way we add ratings information to existed movies.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/rating.png)
* If the movie you input doesn't exist, then you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/rating2.png)

* Then:
http://127.0.0.1:5000/Director/Jack/1972.10.09/theUS/USparty
* This route is the way we add director's information to existed directors.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/dir.png)
* If the director you input doesn't exist, then you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/dir2.png)

* Then:
http://127.0.0.1:5000/Distributor/DreamCo/Los%20Angeles
* This route is the way we add distributor's information to existed distributors.
* you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/dis.png)
* If the distributor you input doesn't exist, then you will see the following image.
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/dis2.png)



## After all, you will get a database with the information you input in.

* Here I show a example which is what I created.
* The database structure:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/structure.png)
* The Ratings and details:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/ratings.png)
* The movies and details:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/movies.png)
* The directors and details:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/directors.png)
* The distributors and details:
* ![Alt text](https://github.com/zuyicai/image/blob/master/project3/distributors.png)


* Exit it / stop it running on the local server by typing `Control + C`
