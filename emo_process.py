import emoji
import sys
import pymongo
from emo_lexicon import emoji_dic
from pymongo import MongoClient

# # # # Database # # # #
MONGO_HOST = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_HOST)


""" all database might be used for this process script """
db0 = client.hashtags_process
db1 = client.emo_process


""" all emotion classification for this process script """
anger1 = db0.anger
excitement1 = db0.excitement
fear1 = db0.fear
happy1 = db0.happy
pleasant1 = db0.pleasant
surprise1 = db0.surprise

anger = db1.anger
excitement = db1.excitement
fear = db1.fear
happy2222 = db1.happy2222
pleasant = db1.pleasant
surprise = db1.surprise



# # # # extract emojis # # # # 
def extract_emojis(text):
    emojis = []
    for char in text:
        if char in emoji.UNICODE_EMOJI:
            emojis.append(char)
    return emojis



# # # # decode emojis # # # # 
def decode_emojis(emojis):
    decoded_emojis = []
    for i in range(0, len(emojis)):
        decoded_emojis.append('U+{:X}'.format(ord(emojis[i])))
    return decoded_emojis



# # # # emo_scoring
def emo_scoring(sample, db_collection, class_name):
    score = {'happy':0,
             'excitement':0,
             'pleasant':0,
             'surprise':0,
             'fear':0,
             'anger':0,}
    emojis = extract_emojis(sample["full_text"])
    decoded_emojis = decode_emojis(emojis)
    for emoji in decoded_emojis:
        if emoji in emoji_dic["anger"]:
            index = emoji_dic["anger"].index(emoji)
            weight = emoji_dic["anger_score"][index]
            score["anger"] += weight
        if emoji in emoji_dic["excitement"]:
            index = emoji_dic["excitement"].index(emoji)
            weight = emoji_dic["excitement_score"][index]
            score["excitement"] += weight
        if emoji in emoji_dic["fear"]:
            index = emoji_dic["fear"].index(emoji)
            weight = emoji_dic["fear_score"][index]
            score["fear"] += weight
        if emoji in emoji_dic["pleasant"]:
            index = emoji_dic["pleasant"].index(emoji)
            weight = emoji_dic["pleasant_score"][index]
            score["pleasant"] += weight
        if emoji in emoji_dic["happy"]:
            index = emoji_dic["happy"].index(emoji)
            weight = emoji_dic["happy_score"][index]
            score["happy"] += weight
        if emoji in emoji_dic["surprise"]:
            index = emoji_dic["surprise"].index(emoji)
            weight = emoji_dic["surprise_score"][index]
            score["surprise"] += weight
    final_class = max(score, key=score.get)
    print(final_class)
    print(score)

    if (score[final_class] == 0) or (final_class == class_name):
        # After hashtag process, filter out the bogus tweets by emo process.
        print("-------------this class-----------------")
        print("final_class: " + final_class)
        print("max score is: " + str(score[final_class]))
        try:
            db_collection.insert_one(sample)
        except pymongo.errors.DuplicateKeyError:
            pass
            print("Data is already in the collection, next one will be processed")



# # # # emo_process # # # #
def emo_process(class_name):
    tweets = db0[class_name].find()
    collection = db1[class_name]
    for tweet in tweets:
        emo_scoring(tweet, collection, class_name)



if __name__ == "__main__":
    emotion_list = ["happy", "anger", "surprise", "pleasant", "excitement", "fear"]

    if len(sys.argv) == 1:
        for class_name in emotion_list:
            emo_process(class_name)

    if len(sys.argv) == 2:
        emotion = str(sys.argv[1])
        emo_process(emotion)
        




