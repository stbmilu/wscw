import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient



# # # # Database for crowdsourcing # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)
db = client.final_tweets

fear = db.fear
happy = db.happy
anger = db.anger
excitement = db.excitement
pleasant = db.pleasant
surprise = db.surprise



# # # # randomly choose 20 tweets for each class # # # #
fear1 = random.sample(list(fear.find()), 20)
happy1 = random.sample(list(happy.find()), 20)
anger1 = random.sample(list(anger.find()), 20)
excitement1 = random.sample(list(excitement.find()), 20)
pleasant1 = random.sample(list(pleasant.find()), 20)
surprise1 = random.sample(list(surprise.find()),20)

tweet_text = []
tweet_id = []
tweet_emotion = []



# # # # store data in csv file # # # # 
def get_tweet_text_for_df(tweets):
    for tweet in tweets:
        tweet_text.append(tweet["full_text"])
        tweet_id.append(tweet["id"])
        tweet_emotion.append(tweet["emotion"])



# # # # generate csv file for crowdsourcing # # # #     
def tweets_to_data_frame(filename):
    get_tweet_text_for_df(fear1)
    get_tweet_text_for_df(happy1)
    get_tweet_text_for_df(anger1)
    get_tweet_text_for_df(excitement1)
    get_tweet_text_for_df(pleasant1)
    get_tweet_text_for_df(surprise1)
    df = pd.DataFrame(data=tweet_text, columns=['tweet_text'])
    df['tweet_id'] = tweet_id
    df['tweet_emotion'] = tweet_emotion
    df.to_csv (os.getcwd() + "/Final_results/crowdsourcing_results/" + filename + ".csv", index=False, header=True)



# # # # anothoer way of creating dataframe csv file # # # #
def tweets_to_data_frame2(tweets, filename):
    """fail due to np array, len([tweet["id"] for tweet in tweets]) = 0 """
    """need to fix this issue"""
    df = pd.DataFrame(data=[tweet["full_text"] for tweet in tweets], columns=['tweets'])
    df['id'] = np.array([tweet["id"] for tweet in tweets])
    df['date'] = np.array([tweet["created_at"] for tweet in tweets])
    df.to_csv (os.getcwd() + "/Final_results/crowdsourcing_results/" + filename + ".csv", index=False, header=True)



if __name__ == "__main__":
    print("The dataset is generated in the path shown as below: ")
    print(os.getcwd()+ "/Final_results/crowdsourcing_results/")
    tweets_to_data_frame("emotion_dataset")

