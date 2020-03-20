# Project Title

This is COMPSCI 5078 web science coursework

## Description

This research aims at collecting 900 reasonably clean tweets with 150 per class.
Emotion class are happy, surprise, excitement, fear, anger and pleasant

### Dependencies

* The main libaray used in this project are:
* tweepy	    3. 8. 0	      For Data fetch
* nltk	        3. 4. 5	      For Text process
* emoji	        0. 5. 4	      For Text process
* numpy	        1. 17. 2	  For Extract results
* pymongo	    3. 10. 1	  For Data store
* pandas	    1. 0. 1	      For Data to csv file
* contractions	0. 0. 24	  For Text process

## Getting Started
For data fetch. Both streaming API and rest API can be used in this project.<br>
The program should be run in the following order:<br><br>
1.collectdata.py. (specify a emotion and a data fetch method in commond line) fetch method includes "rest" and "stream".<br>
  This project include two data fetch method in this stript.<br>
  e.g. python3 collectdata.py happy rest<br><br><br>


2.hashtag_process.py. (specify a emotion or a method) method inclues "rest", "stream" and "mix", which indicates the database.<br>
Since some user might use hybird approach to fetch data(both rest and stream)<br>
  e.g. python3 hashtag_process.py happy rest.<br>
  e.g. python3 hashtag_process.py happy.<br>
  if you don't include the method, this program will use "rest" database by default.<br>

```
 3.emo_process.py (you can alterntively specify a emotion class, or process all classes by default.)
  e.g. python3 emo_process.py happy
  e.g. python3 emo_process.py 
```

* 4.text_process.py (you can alterntively specify a emotion class, or process all classes by default.)
*  e.g. python3 text_process.py happy
*  e.g. python3 text_process.py
*  Notes:if you see the error like nltk.download('punkt'), please run fix_nltk.py, and download the language package you want.

* After data process, our data can be analysis by the following scripts:
* 1.cs_to_csv.py ---> generates 120 tweets for crowdsourcing, make sure you have at least 20 tweets per emotion collection.

* 2.extract_final_results.py ---> extract final 900 tweets with both orignial text and processed text, the database used is final_tweets.
* (you can alterntively specify a emotion class, or process all classes by default.)
*   e.g. python3 extract_final_results.py happy
*   e.g. python3 extract_final_results.py
   
* 3.extract_raw_data.py ---> extract raw data. (you can alterntively specify a emotion class, or process all classes by default.)
*  e.g. python3 extract_raw_data.py happy
*  e.g. python3 extract_raw_data.py

* 4.cs_results_analysis.py ---> analysis the crowdsourcing reports

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```
