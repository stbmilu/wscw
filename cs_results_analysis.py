import os
import csv
import pandas as pd


# # # # full report dictionary # # # #
full_report = {"happy":{"correct_amount":0, "total_amount": 0},
               "anger":{"correct_amount":0, "total_amount": 0},
               "surprise":{"correct_amount":0, "total_amount": 0},
               "excitement":{"correct_amount":0, "total_amount": 0},
               "fear":{"correct_amount":0, "total_amount": 0},
               "pleasant":{"correct_amount":0, "total_amount": 0},}



# # # # relevant dataframe # # # #
emotion_list = []
correct_amount = []
total_amount = []
rate = []



# # # # loop through the results file to get successful rate # # # #
def get_successful_rate():
    with open("crowdsourcing_reports/f1558973_full_report_updated.csv", "r") as results:
        reader = csv.DictReader(results)
        for row in reader:
            full_report[row['tweet_emotion']]['total_amount'] += 1
            """ In the crowdsourcing, this research set value 1,2,3,4,5,6, 
                as happy, pleasant, surprise, anger, fear, and excitement
            """
            if row['tweet_emotion'] == "happy":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "1":
                    full_report[row['tweet_emotion']]["correct_amount"] += 1
            if row['tweet_emotion'] == "pleasant":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "2":
                    full_report[row['tweet_emotion']]["correct_amount"] += 1
            if row['tweet_emotion'] == "surprise":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "3":
                    full_report[row['tweet_emotion']]["correct_amount"] += 1
            if row['tweet_emotion'] == "anger":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "4":
                    full_report[row['tweet_emotion']]["correct_amount"] += 1
            if row['tweet_emotion'] == "fear":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "5":
                    full_report[row['tweet_emotion']]["correct_amount"] += 1
            if row['tweet_emotion'] == "excitement":
                if row['what_is_the_authors_sentiment_feeling_in_this_text_or_what_emotion_does_this_text_convey'] == "6":
                   full_report[row['tweet_emotion']]["correct_amount"] += 1
    
    for k, value in full_report.items():
        emotion_list.append(k)
        correct_amount.append(value["correct_amount"])
        total_amount.append(value["total_amount"])
        rate.append("{0:.0f}%".format(value["correct_amount"]/value["total_amount"] * 100))



# # # # generate analysis results # # # #
def analysis_results(class_name):
    df = pd.DataFrame(data=emotion_list, columns=['emotion'])
    df["agreement_amount"] = correct_amount
    df["judgement_amount"] = total_amount
    df["agreement_rate"] = rate
    df.to_csv (os.getcwd() + "/Final_results/crowdsourcing_results/" + class_name + ".csv", index=False, header=True)



if __name__ == "__main__":
    print("The analysis csv file is generated in the path shown as below: ")
    print(os.getcwd()+ "/Final_results/crowdsourcing_results/")
    get_successful_rate()
    analysis_results("crowdsourcing_analysis")

