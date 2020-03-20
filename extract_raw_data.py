import os
import sys
import pandas as pd
import pymongo
from pymongo import MongoClient



# # # # Database for hashtag process # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)
db = client.rest_twitter_database
db0 = client.streaming_twitter_database
""" the actuall database used for raw data is:
    db = client.cursor_database
"""
""" you could also use
    db1 = client.rest_twitter_database
    db2 = client.streaming_twitter_database
    db3 = client.duplicate_pre_process_rest
    db4 = client.duplicate_pre_process_stream
    db5 = client.duplicate_pre_process_mix
    as well
"""
fear = db.fear
happy = db.happy
anger = db.anger
excitement = db.excitement
pleasant = db.pleasant
surprise = db.surprise



# # # # Buffer for each class # # # #
tweet_id = []
tweet_created_at = []
tweet_full_text = []
tweet_lang = []



# # # # get data required # # # #
def get_tweet_text_for_df(class_name):
    tweets = db[class_name].find()
    dic = {"tweet_id": [],
           "tweet_lang": [],
           "tweet_created_at": [],
           "tweet_full_text": [],
           }
    for tweet in tweets:
        dic["tweet_full_text"].append(tweet["full_text"])
        dic["tweet_id"].append(tweet["id"])
        dic["tweet_lang"].append(tweet["lang"])
        dic["tweet_created_at"].append(tweet["created_at"])
    return dic



# # # # generate csv file for final results # # # #
def tweets_to_data_frame(class_name):
    dic = get_tweet_text_for_df(class_name)
    df = pd.DataFrame(data=dic["tweet_id"], columns=['tweet_id'])
    df["tweet_full_text"] = dic["tweet_full_text"]
    df['tweet_lang'] = dic["tweet_lang"]
    df['created_at'] = dic["tweet_created_at"]
    df.to_csv (os.getcwd() + "/Raw_data/" + class_name + ".csv", index=False, header=True)



if __name__ == "__main__":
    
    emotion_list = ["happy", "anger", "surprise", "pleasant", "excitement", "fear"]
    if len(sys.argv) == 2:
        emotion = str(sys.argv[1])
        if emotion in emotion_list:
            tweets_to_data_frame(emotion)
        else:
            print("One of the input arguement is not correct, please try again!")
            
    if len(sys.argv) == 1:
        tweets_to_data_frame("happy")
        tweets_to_data_frame("anger")
        tweets_to_data_frame("surprise")
        tweets_to_data_frame("excitement")
        tweets_to_data_frame("fear")
        tweets_to_data_frame("pleasant")
