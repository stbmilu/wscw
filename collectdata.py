import pymongo
import json
import sys
import os
import datetime
import random
import time
from pymongo import MongoClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor


# # # # Credentials # # # #
'''
Variables that contain credentials to access Twitter API.
'''
ACCESS_TOKEN = "1232366099158773765-wqyFQ36xv6VAsKNeD1xE3a1zhjQzfv"
ACCESS_TOKEN_SECRET = "Tcc3WkeXbpyjwVyiSoqi0PlADJM8Fq9G4leTATyWfTheU"
CONSUMER_KEY = "4JeS4XmXDhnmyT450OVUZ8HIO"
CONSUMER_SECRET = "Z2rr8mX1klV1nqMGoWGPmnO00mwTiPhzQHD6FuWLSqZXJ3S6RL"


# # # # Twitter database # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)
db = client.twitter_database
db_for_cursor = client.cursor_database

db1 = client.streaming_twitter_database
db2 = client.rest_twitter_database



# # # # Twitter Cursor API # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.api = API(self.auth, wait_on_rate_limit=True)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.api

    def cursor_data(self, query, db_collection, amount):
        #tweepy.Cursor(API.search, q="$EURUSD", count=1000, tweet_mode='extended', lang='en').items()
        for tweet in Cursor(self.api.search, q=query, lang="en", tweet_mode='extended').items(amount):
            db_collection.insert_one(tweet._json)
            print(tweet._json["full_text"])
            #print('----- if you see the program stop running, it might reach the api limitation, -----')
            #print('----- please wait for few minutes and restart the program -----')


# # # # Twitter Authenticater # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth
        


# # # # Twitter Streamer # # # #
class TwitterStreamer():
    '''
    Class for streaming and processing live tweets.
    '''
    def __init__ (self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, tweets_filename, collection, max, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter streaming API
        auth = self.twitter_authenticator.authenticate_twitter_app()
        listener = TwitterListener(tweets_filename, collection, max)
        stream = Stream(auth, listener)

        # This line filter Twitter streams to capture data by the keywords:
        stream.filter(track=hash_tag_list, languages=["en"])



# # # # Twitter Streamer Listener # # # #
class TwitterListener(StreamListener):
    
    '''
    Class for listener and storing data
    '''
    def __init__(self, tweets_filename, collection, max):
        self.tweets_filename = tweets_filename
        self.collection = collection
        self.i = 0
        self.max = max

    def on_data(self, data):

        try:
            print(data)
            with open(self.tweets_filename, 'a') as tf:
                tf.write(data)
            data_json = json.loads(data)
            self.collection.insert_one(data_json)
            self.i = self.i + 1
            if self.i< self.max:
                return True
            else:
                return False

        except BaseException as e:
            print("Error on_data %s" % str(e))

    def on_error(self, status):
        # print the status message of the error
        print(status)



# # # # hashtag query # # # # 
query_dic = {
"happy":     ["#happy", "#joy", "#love", "#like", "#good", 
              "#glad", "#better", "#rejoice", "#innerpeace", "#blessed"],         #joy <--> happy

"excitement":["#excitement", "#believing", "#ambition", "#exciting", "#music", 
              "#predictable", "#delight", "#interesting", "#expected", "#hobby"], #anticipation <--> excitement

"pleasant":  ["#pleasant", "#smile", "#pride", "#motivation", "#trusted",
              "#acceptance", "#beautiful", "#sweet", "#comfortable", "#welcome", 
              "#admiration", "#admiring", "#loyal"],                              #pleasant <--> trust

"surprise":  ["#suprise", "#amazing", "#wonder", "#preoccupied", "#amazement", 
              "#astonishment", "#great", "#lol", "#cool", "#funny", "#sad", 
              "#frustration", "#sorrowful", "#sadness"],                          #sadness suprise <--> suprise

"fear":      ["#fear", "#fearful", "#danger", "#apprehension", "#apprehensive",
              "#freakout", "#fearing", "#anxiety", "#panic", "#terror", "#bigot", 
              "#sickened", "#hateful", "#dislike", "#foul"],                      #fear digust <--> fear

"anger":     ["#anger", "#agitated", "#roar", "#hormonal", "#fuckedoff",
              "#sogay", "#aggressive", "#furious", "#angry", "#annoyance", 
              "#hostility", "#enraged", "#fustrated"],                            # anger <--> Anger
}



# # # # streaming data fetch # # # #
def streaming_data_fetch(class_name, db_collection, amount):
    starttime = datetime.datetime.now()
    tweets_filename = class_name + ".json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(tweets_filename, db_collection, amount, query_dic[class_name])
    endtime = datetime.datetime.now()
    duration = (endtime - starttime).seconds
    print("-------------------------------")
    print("End of the fetching, time duration: " + str(duration))



# # # # rest data fetch # # # #
def rest_data_fetch(class_name, db_collection):
    starttime = datetime.datetime.now()
    Rest_api = TwitterClient()
    for i in range(0, 4):
        query = random.sample(query_dic[class_name], 1)
        Rest_api.cursor_data(query, db_collection, 250)
    endtime = datetime.datetime.now()
    duration = (endtime - starttime).seconds
    print("-------------------------------")
    print("End of the fetching, time duration: " + str(duration))




if __name__ == "__main__":

    print("working dir:" +os.getcwd())
    print("Python version:"+sys.version)
    print("-------------------------------------------------------------------------------------------------------------------")
    print('Let\'s start tweet data fetching')
    print("\n--------------Instruction------------------------------------------------------------------------------------------\n")
    print("This program takes 20 seconds for user to read the instruction.")
    print("If you use streaming api, program might take a long time for 1000 tweets collection.")
    print("If you use rest api, program could reach querying limitation if you see fetching stops at the middle of the process.")
    print("Solution: take a rest for few minutes, and restart the program.")
    print("\n-------------Amount of tweets---------------------------------------------------------------------------------------\n")
    print("It is expected to fetch 1000 tweets per collection, however rest api collection is limited due to different keyword.")
    print("The actual amount collected by rest api is near or equal to 1000.")
    print("The actual amount collected by streaming api would definitely be 1000 as long as you could wait.")
    print("\n--------------------------------------------------------------------------------------------------------------------\n")

    time.sleep(20)
    emotion = str(sys.argv[1])
    method = str(sys.argv[2])


    """ streaming data fetch """
    if emotion == "happy" and method == "stream":
        streaming_data_fetch(emotion, db1.happy, 1000)

    if emotion == "anger" and method == "stream":
        streaming_data_fetch(emotion, db1.anger, 1000)

    if emotion == "pleasant" and method == "stream":
        streaming_data_fetch(emotion, db1.pleasant, 1000)

    if emotion == "excitement" and method == "stream":
        streaming_data_fetch(emotion, db1.excitement, 1000)

    if emotion == "surprise" and method == "stream":
        streaming_data_fetch(emotion, db1.surprise, 1000)

    if emotion == "fear" and method == "stream":
        streaming_data_fetch(emotion, db1.fear, 1000)



    """ rest data fetch """
    if emotion == "happy" and method == "rest":
        rest_data_fetch(emotion, db2.happy)
    
    if emotion == "anger" and method == "rest":
        rest_data_fetch(emotion, db2.anger)

    if emotion == "pleasant" and method == "rest":
        rest_data_fetch(emotion, db2.pleasant)

    if emotion == "excitement" and method == "rest":
        rest_data_fetch(emotion, db2.excitement)

    if emotion == "surprise" and method == "rest":
        rest_data_fetch(emotion, db2.surprise)

    if emotion == "fear" and method == "rest":
        rest_data_fetch(emotion, db2.fear)
