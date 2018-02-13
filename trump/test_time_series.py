import tweepy
from tweepy import OAuthHandler
import sys
import json
import pandas as pd
import operator
import os
import matplotlib.pyplot as plt
import numpy as np
import config
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

"""
Using the tutorial, testing to see the format of the twitter data,as mine seems to be duplicated and weird.
"""

def twitter_setup():
    """Initiate API"""
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)
    return(api)

extractor = twitter_setup()
# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 5 tweets:
print("5 recent tweets:\n")
for tweet in tweets[:5]:
        print(tweet.text)
        print()

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])

tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

tret.plot(figsize=(16,4), color='r')

