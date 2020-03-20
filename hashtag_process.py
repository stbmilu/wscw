import json
import pymongo
import pandas as pd
import re
import sys
from pymongo import MongoClient



# # # # Database for hashtag process # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)

""" 
the database used for raw data

db0 = client.twitter_database
db = client.hashtag_process
db1 = client.cursor_database
db2 = client.remove_duplicates

"""

""" all database might be used for this process script """
db1 = client.rest_twitter_database
db2 = client.streaming_twitter_database
db3 = client.duplicate_pre_process_rest
db4 = client.duplicate_pre_process_stream
db5 = client.duplicate_pre_process_mix
db6 = client.hashtags_process

""" all emotion classification for this process script """
anger = db6.anger
anger222 = db6.anger222
happy = db6.happy
excitement = db6.excitement
pleasant = db6.pleasant
surprise = db6.surprise
fear = db6.fear


# # # # NRC Emotional Lexicon # # # #
filepath = "NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
lexicon = pd.read_csv(filepath, names=["Class", "hashtag", "association"], skiprows=45, sep='\t')



# # # # get full texts for streaming api collected tweets # # # #
def get_full_text_stream(db_collection1):
    tweets = db_collection1.find()
    for tweet in tweets:
        if ("retweeted_status" in tweet):
            try:
                tweet["full_text"] = tweet["retweeted_status"]["extended_tweet"]["full_text"]
            except:
                tweet["full_text"] = tweet["retweeted_status"]["text"]
        else:
            try:
                tweet["full_text"] = tweet["extended_tweet"]["full_text"]
            except KeyError:
                tweet["full_text"] = tweet["text"]
        print("-------------------------the tweet full text ---------------------------------")
        print(tweet["full_text"])



# # # # get full texts for rest api collected tweets # # # #
def get_full_text_stream(db_collection1):
    tweets = db_collection1.find()
    for tweet in tweets:
        print("-------------------------the tweet full text ---------------------------------")
        print(tweet["full_text"])



# # # # Remove Duplicate Tweets by rest api fetch # # # #
def remove_duplicates_rest(db_collection1, db_collection2):
    tweets = db_collection1.find()
    tweet_text_list = []
    for tweet in tweets:
        if tweet["full_text"] not in tweet_text_list:
            tweet_text_list.append(tweet["full_text"])
            try:
                db_collection2.insert_one(tweet)
            except pymongo.errors.DuplicateKeyError:
                """ in case the raw data is not enough,
                    don't need to delete the collection
                    and restart again
                """
                continue



# # # # Remove Duplicate Tweets by stream api fetch # # # #
def remove_duplicates_stream(db_collection1, db_collection2):
    tweets = db_collection1.find()
    tweet_text_list = []
    for tweet in tweets:
        if ("retweeted_status" in tweet):
            try:
                tweet["full_text"] = tweet["retweeted_status"]["extended_tweet"]["full_text"]
            except:
                tweet["full_text"] = tweet["retweeted_status"]["text"]
        else:
            try:
                tweet["full_text"] = tweet["extended_tweet"]["full_text"]
            except KeyError:
                tweet["full_text"] = tweet["text"]
        if tweet["full_text"] not in tweet_text_list:
            tweet_text_list.append(tweet["full_text"])
            try:
                db_collection2.insert_one(tweet)
            except pymongo.errors.DuplicateKeyError:
                """ in case the raw data is not enough,
                    don't need to delete the collection
                    and restart again
                """
                continue



# # # # tweet hashtag process # # # #
def hashtag_process(tweet, db_collection, class_name):
    score = {"happy": 0,
             "surprise": 0,
             "pleasant": 0,
             "excitement": 0,
             "fear": 0,
             "anger": 0,}
    text = tweet["full_text"]

    """This step extract all hashtags into an array"""
    hashtag = [i for i in text.split() if i.startswith("#")]

    for h in hashtag:
        for i in range(len(lexicon[lexicon.hashtag == h].Class.values)):
            emotion = lexicon[lexicon.hashtag == h].Class.values[i]
            weight = lexicon[lexicon.hashtag == h].association.values[i]
            if emotion == "anger" or emotion == "sadness":
                score["anger"] += weight
            if emotion == "fear" or emotion == "disgust":
                score["fear"] += weight
            if emotion == "anticipation":
                score["excitement"] += weight
            if emotion == "joy":
                score["happy"] += weight
            if emotion == "surprise":
                score["surprise"] += weight
            if emotion == "trust":
                score["pleasant"] += weight
    final_class = max(score, key=score.get)
    if (score[final_class] > 0) and (final_class == class_name):
        print(text)
        print("-------------classification approved-----------------------------------------")
        print(str(score))
        print("Final classification: " + final_class)
        print("Final score: " + str(score[final_class]))
        try:
            db_collection.insert_one(tweet)
        except pymongo.errors.DuplicateKeyError:
            pass
            print("Data is already in the collection, next one will be processed")
    
    elif (score[final_class] == 0):
        """ text with no score should be considered as spam tweet in this research """
        pass



# # # # final hashtag process # # # #
def emotion_hashtag_process(class_name, emotion_collection, fetch_method):
    if fetch_method == "rest":
        raw_collection = db1[class_name]
        duplicate_process_collection = db3[class_name]
        remove_duplicates_rest(raw_collection, duplicate_process_collection)
        tweets = duplicate_process_collection.find()
    if fetch_method == "stream":
        raw_collection = db2[class_name]
        duplicate_process_collection = db4[class_name]
        remove_duplicates_stream(raw_collection, duplicate_process_collection)
        tweets = duplicate_process_collection.find()
    if fetch_method == "mix":
        raw_collection1 = db1[class_name]
        raw_collection2 = db2[class_name]
        duplicate_process_collection = client.mix_twitter_database[class_name]
        duplicate_process_collection2 = db5[class_name]
        remove_duplicates_rest(raw_collection1, duplicate_process_collection)
        remove_duplicates_stream(raw_collection2, duplicate_process_collection)
        remove_duplicates_rest(duplicate_process_collection, duplicate_process_collection2)
        client.drop_database('mix_twitter_database')
        tweets = duplicate_process_collection2.find()
    for tweet in tweets:
        hashtag_process(tweet, emotion_collection, class_name)
    
    

if __name__ == "__main__":

    emotion_list = ["happy", "anger", "surprise", "pleasant", "excitement", "fear"]
    method_list = ["rest", "stream", "mix"]
    if len(sys.argv) == 3:
        emotion = str(sys.argv[1])
        method = str(sys.argv[2])
        if (emotion in emotion_list) and (method in method_list):
            emotion_hashtag_process(emotion, db6[emotion], method)
        else:
            print("One of the input arguement is not correct, please try again!")
            
    if len(sys.argv) == 2:
        emotion = str(sys.argv[1])
        if emotion in emotion_list:
            emotion_hashtag_process(emotion, db6[emotion], "rest")
        else:
            print("Emotion class is not in the required list, please try again!")

    if len(sys.argv) == 1:
        print("Please enter a emotion name in commond line, please try again!")

    
    




