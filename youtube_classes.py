import re
from db_manager import Base, db_session
from sqlalchemy import Column, Integer, String
from googleapiclient.discovery import build
from flask import request

# Sets up YouTube API builder parameters
KEY = 'AIzaSyCQ4O1W27gujjdwS1ouAj3kUm2v49ANj7o'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class Settings(Base):
    __tablename__ = 'settings'

    # Sets up Columns in database for Settings class
    user_id = Column(Integer, primary_key=True)

    def __init__(self, results_regex='.*',
                        maxResults=50,
                        reverseResults=False):
        
        # Sets all of the attributes for the Settings object
        self.results_regex = results_regex
        self.maxResults = maxResults
        self.reverse_results = reverseResults

    def __repr__(self) -> str:
        return super().__repr__()
    
class Search(Base):
    __tablename__ = 'searches'

    # Sets up Columns in database for Search class
    id = Column(Integer, primary_key=True)
    searchPhrase = Column(String)

    def __init__(self, searchPhrase: str, settings: Settings):

        # Sets all of the attirbutes for the Search object
        self.searchPhrase = searchPhrase
        self.settings = settings

    def scrape(self):

        # Builds YouTube API client using API Key
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=KEY)

        # Scrapes YouTube API
        search_response = youtube.search().list(
            q=request.args.get('q') or self.searchPhrase,
            type='video',
            part='id,snippet',
            maxResults=self.settings.maxResults
        ).execute()
        # print(search_response)

        self.search_results = search_response['items']
        
        # Checks to make sure that the API returns search results; if not, prints error message
        if not self.search_results:
            return 'Error: No YouTube results'
        
        # initializes list of Video objects
        self.videoList = [Video(videoData=search_result) for search_result in self.search_results]

        # add videos to database
        for video in self.videoList:
            db_session.add(video)
        db_session.commit()

    def sortVideoList(self):
        # accounts for regex setting
        for video in self.videoList:
            if not re.search(pattern=self.settings.results_regex, string=video.videoTitle):
                self.videoList.remove(video)

        # accounts for reverse setting
        if self.settings.reverse_results:
            self.videoList.reverse()

class Video(Base):
    __tablename__ = 'videos'

    # Sets up Columns in database for Video class
    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __init__(self, videoData):
        
        # Sets the Video's attributes from the passed in data
        videoId = videoData['id']['videoId']
        self.url = f'https://youtu.be/{videoId}'
        self.videoTitle = videoData['snippet']['title']
        self.description = videoData['snippet']['description']
        self.channelTitle = videoData['snippet']['channelTitle']
        self.datePublished = videoData['snippet']['publishedAt'][:10]
        self.thumbnail_url = videoData['snippet']['thumbnails']['high']['url']
