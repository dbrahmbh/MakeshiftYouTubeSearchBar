import os
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, request, render_template, redirect, url_for
from db_manager import db_session
from youtube_classes import Settings, Search, Video
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

# Makes Flask app
app = Flask(__name__)
Bootstrap(app)
Markdown(app)

# Sets global varibles so that they can used in different routes
keySearch = None
setr = Settings()

# Main Page - Search Bar
@app.route('/', methods=["GET", "POST"])
def searchBar():
    global keySearch
    global setr

    # If there is a GET request, display the search bar using the searchbar template
    if request.method == "GET":
        return render_template('searchbar.html')
    
    # Requests search keyphrase from HTML form and redirects to results page
    if request.method == "POST":
        keyPhrase = request.form.get("phrase")
        # print(keyPhrase)
        
        # Adds keyPhrase to database and saves it (search history)
        keySearch = Search(searchPhrase=keyPhrase, settings=setr)
        db_session.add(keySearch)
        db_session.commit()

        return redirect(url_for('yt'))

# Results Page
@app.route('/results/')
def yt():
    global keySearch

    # Clears video entries in database so that entries do not pile up
    try:
        videos = Video.query.all()
        for video in videos:
            db_session.delete(video)
        db_session.commit()
    except:
        pass

    # Scrapes YouTube API for search results
    keySearch.scrape()

    # Applies filters from Settings object to video list before being shown on the web page
    keySearch.sortVideoList()

    # Returns template that shows results
    return render_template('results.html', videoList=keySearch.videoList)

# Filters Page
@app.route('/filters/', methods=["GET", "POST"])
def filters():
    global setr

    # If there is a GET request, display the filters page using the filters template
    if request.method == "GET":
        return render_template('filters.html', setr=setr)
    
    # Sets the attributes of the Settings class to whatever the user submitted through the HTML form
    if request.method == "POST":
        
        setr.results_regex = request.form.get('results_regex', None)
        setr.maxResults = int(request.form.get('maxResults', None))
        if request.form.get('reverse_results', None) == "True":
            setr.reverse_results = True
        else:
            setr.reverse_results = False

        return render_template('filters.html', setr=setr)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Runs the app when ran from the command line
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))