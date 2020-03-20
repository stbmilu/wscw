# wscw
This is COMPSCI5078 individual coursework 2020

The database used in this project is MONGODB, MONGO_HOST = 'mongodb://localhost:27017/'.

The program should be run in the following order:\n
1.collectdata.py. (specify a emotion and a data fetch method in commond line) fetch method includes "rest" and "stream".This project include two data fetch method in this stript.
  e.g. python3 collectdata.py happy rest
2.hashtag_process.py. (specify a emotion or a method) method inclues "rest", "stream" and "mix", which indicates the database.Since some user might use hybird approach to fetch data(both rest and stream)
  e.g. python3 hashtag_process.py happy rest. 
  e.g. python3 hashtag_process.py happy
  if you don't include the method, this program will use "rest" database by default.
3.emo_process.py (you can alterntively specify a emotion class, or process all classes by default.)
  e.g. python3 emo_process.py happy
  e.g. python3 emo_process.py 
4.text_process.py (you can alterntively specify a emotion class, or process all classes by default.)
  e.g. python3 text_process.py happy
  e.g. python3 text_process.py
  Notes:if you see the error like nltk.download('punkt'), please run fix_nltk.py, and download the language package you want.


After data process, our data can be analysis by the following scripts:
1.cs_to_csv.py ---> generates 120 tweets for crowdsourcing, make sure you have at least 20 tweets per emotion collection.

2.extract_final_results.py ---> extract final 900 tweets with both orignial text and processed text, the database used is final_tweets.(you can alterntively specify a emotion class, or process all classes by default.)
  e.g. python3 extract_final_results.py happy
  e.g. python3 extract_final_results.py
  
3.extract_raw_data.py ---> extract raw data. (you can alterntively specify a emotion class, or process all classes by default.)
  e.g. python3 extract_raw_data.py happy
  e.g. python3 extract_raw_data.py
4.cs_results_analysis.py ---> analysis the crowdsourcing reports





