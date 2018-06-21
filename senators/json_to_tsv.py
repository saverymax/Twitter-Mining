import tweepy
import sys
import json
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import plotly_credentials


class tweetflow():
    """
    Class to save tweet to tsv, and clean tweet in order to produce bar graphs of frequent words for initial analysis.
    The cleaning doesn't necessarily belong here, but here it is due to the way I've built this pipeline.
    """

    def __init__(self, path):
        """Initiate instance of tweet jsonl."""
        
        print("init conversion of jsonl to tsv")
        self.path = path

    def read_tweets(self):
        """
        Read tweets saved in the jsonl file, preprocess the text, and save tweets in a csv and a list. These will be filtered and visualized later.
        """
        # Create an array to hold the content of the tweets.
        terms_in_tweets = []
        tweet_list = []
        tweet_date = []
        tweet_likes = []
        tweet_RT = []
        username = []
        
        # Read and process tweets. See above functions
        with open('data/search.jsonl', 'r') as infile:
            for line in infile:
                tweet = json.loads(line)
                # next 2 lines just for search:
                try:
                    tweet_list.append(tweet['full_text'])
               
                except KeyError as e:
                    print("Key error in jsonl conversion:", e)

                tweet_date.append(tweet['created_at'])
                tweet_RT.append(tweet['retweet_count'])
                tweet_likes.append(tweet['favorite_count'])
                username.append(tweet['user']['screen_name'])

        # Create dataframe to be used for time series and sentiment analysis
        tweet_dataframe = pd.DataFrame({
            'username': username, 
            'text': tweet_list, 
            'retweets': tweet_RT, 
            'likes': tweet_likes, 
            'date': tweet_date})

        tweet_dataframe.to_csv(
                '{}converted_tweets.tsv'.format(self.path), 
                sep='\t', 
                index = False)
