import re
import contractions
import string
import nltk
import sys
import pymongo
from string import ascii_lowercase, punctuation
from pymongo import MongoClient
from autocorrect import spell

#nltk.download('punkt')

# # # # Database for hashtag process # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)
db1 = client.emo_process
db2 = client.final_tweet

'''db_collections of all emo_processed classes'''
fear1 = db1.fear
happy1 = db1.happy
anger1 = db1.anger
excitement1 = db1.excitement
pleasant1 = db1.pleasant
surprise1 = db1.surprise

'''db_collections of all final tweets'''
fear = db2.fear
happy = db2.happy
anger = db2.anger
excitement = db2.excitement
pleasant = db2.pleasant
surprise = db2.surprise


# # # # modified string library # # # #
""" 1, for punctuation delete.
    2, for duplicated chars e.g. loooooove
"""
punct_dic = punctuation
useful_punct = "!,.:?;"
for char in useful_punct:
    punct_dic = punct_dic.replace(char, "")

duplicate_chars = {}
for char in ascii_lowercase:
    duplicate_chars[char] = re.compile(char + r'{3,}')



# # # # clean methods # # # #

def remove_url(sample):
    """Remove URLs from a sample string"""
    sample["full_text"] = re.sub(r"http\S+", "", sample["full_text"])
    return sample


def replace_contractions(sample):
    """Replace contractions in string of text"""
    sample["full_text"] = contractions.fix(sample["full_text"])
    return sample


def remove_RT_and_mentions(sample):
    """1. Remove the RT @name in a tweet,
       2. Remove other mentions in this tweet
    """
    sample["full_text"] = re.sub('RT @[\w_]+: ', '', sample["full_text"])
    sample["full_text"] = re.sub(r"@(\w+)", '', sample["full_text"], flags=re.MULTILINE)
    return sample


def remove_last_few_hashtags_behind_a_core_sentence(sample):
    """1.remove last few hashtags behind the main sentence
       2.keep the hashtags which at the middle of the sentence
    """
    sample["full_text"] = re.sub(r"#[\w-]+(?=(?:\s+#[\w-]+)*\s*$)", '', sample["full_text"], flags=re.MULTILINE)
    #sample["full_text"] = re.sub(r"( #\S+)*$", '', sample["full_text"], flags=re.MULTILINE)
    return sample


def correct_spelling(sample):
    """ correct the spelling, e.g. looooove to love """
    words = nltk.word_tokenize(sample["full_text"])
    for word in words:
        for char, duplicate_char in duplicate_chars.items():
            word = re.sub(duplicate_char, char, word)
    #sample["full_text"] = ' '.join([spell(w)] for w in tweet.split()])
    sample["full_text"] = ' '.join([w for w in words])
    return sample


def remove_punct(sample):
    """ 1.as mentioned before, remove unnecessary punctuations
        2.keep chars as !,.:?; which might be useful for analysis one text.
    """
    sample["full_text"]  = "".join([char for char in sample["full_text"] if char not in punct_dic])
    return sample



# # # # text process for one tweet# # # #
def text_process(sample):
    print("--------------------------------the original full text---------------------------------")
    print(sample["full_text"])
    sample = remove_RT_and_mentions(sample)
    sample = remove_url(sample)
    sample = replace_contractions(sample)
    sample = remove_last_few_hashtags_behind_a_core_sentence(sample)
    sample = correct_spelling(sample)
    sample = remove_punct(sample)
    print("--------------------------------the processed full text---------------------------------")
    print(sample["full_text"])
    return sample
    

# # # # process final tweets and remove duplicates # # # #
def process_final_tweets_and_remove_duplicates(db_collection1, db_collection2, emotion, max_amount):
    tweets = db_collection1.find()
    tweet_text_list = []
    for tweet in tweets:
        tweet["original_text"] = tweet["full_text"]
        text_process(tweet)
        count = db_collection2.count()
        if count == 0:
            count = 0
        if tweet["full_text"] not in tweet_text_list:
            tweet_text_list.append(tweet["full_text"])
            tweet["emotion"] = emotion
            if count < max_amount:
                try:
                    db_collection2.insert_one(tweet)
                except pymongo.errors.DuplicateKeyError:
                    pass
                    print("Data is already in the collection, next one will be processed")
                
    """if data is not enough offer user a prompt to collect more data"""
    if count < max_amount:
        print("need more data for final classification")


if __name__ == "__main__":

    if len(sys.argv) == 2:
        emotion = str(sys.argv[1])
        process_final_tweets_and_remove_duplicates(db1[emotion], db2[emotion], emotion, 150)

    if len(sys.argv) == 1:
        try:
            process_final_tweets_and_remove_duplicates(db1["fear"], db2["fear"], "fear", 150)
        except UnboundLocalError:
            print("Fear raw data is empty! Please collect more data.")

        try:
            process_final_tweets_and_remove_duplicates(db1["happy"], db2["happy"], "happy", 150)
        except UnboundLocalError:
            print("Happy raw data is empty! Please collect more data.")

        try:
            process_final_tweets_and_remove_duplicates(db1["anger"], db2["anger"], "anger", 150)
        except UnboundLocalError:
            print("Anger raw data is empty! Please collect more data.")

        try:
            process_final_tweets_and_remove_duplicates(db1["surprise"], db2["surprise"], "surprise", 150)
        except UnboundLocalError:
            print("Surprise raw data is empty! Please collect more data.")

        try:
            process_final_tweets_and_remove_duplicates(db1["excitement"], db2["excitement"], "excitement", 150)
        except UnboundLocalError:
            print("Excitement raw data is empty! Please collect more data.")

        try:
            process_final_tweets_and_remove_duplicates(db1["pleasant"], db2["pleasant"], "pleasant", 150)
        except UnboundLocalError:
            print("Pleasant raw data is empty! Please collect more data.")
