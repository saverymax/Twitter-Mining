import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
    likes_series = pd.Series(data = tweet_dataframe['likes'].values, index = tweet_dataframe['date'])
    retweets_series = pd.Series(data=tweet_dataframe['retweets'].values, index=tweet_dataframe['date'])
    #polarity_series = pd.Series(data=tweet_dataframe['polarity'].values, index=tweet_dataframe['date'])
    #subjectivity_series = pd.Series(data=tweet_dataframe['subjectivity'].values, index=tweet_dataframe['date'])
    
    likes_series.plot(figsize = (32,8), color = 'g', label = 'Likes', legend = True)
    retweets_series.plot(figsize = (32,8), color = 'r', label = 'Retweets', legend = True)
    #polarity_series.plot(figsize = (32,8), color = 'y', label = 'polarity', legend = True)
    #subjectivity_series.plot(figsize = (32,8), color = 'b', label = 'subjectivity', legend = True)
    
    plt.savefig("{0}.png".format("time_series"), bbox_inches = 'tight') 
    plt.show()
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

tweet_data = pd.read_csv("converted_tweets_sentiment.tsv", sep = '\t', parse_dates=[2]) 

# print(type(tweet_data['date'][1])) # confirms that date is a <class 'pandas.tslib.Timestamp'> 
time_series(tweet_data)
