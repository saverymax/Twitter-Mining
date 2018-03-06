import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
    likes_series = pd.Series(data = tweet_dataframe['likes'].values, index = tweet_dataframe['date'])
    
    retweets_series = pd.Series(data=tweet_dataframe['retweets'].values, index=tweet_dataframe['date'])

    subjectivity_series = pd.Series(data=tweet_dataframe['subjectivity'].values, index=tweet_dataframe['date'])
    
    polarity_series = pd.Series(data=tweet_dataframe['polarity'].values, index=tweet_dataframe['date'])
   
    time_series_figure, (axis1, axis2) = plt.subplots(2,1, figsize = (32,16), sharex = True)
    time_series_figure.suptitle("Trumps 500 most recent tweets")
    axis1.set_title("likes and retweet frequency of Trump's tweets")
    axis1.plot(likes_series, color = "b", label = "likes")
    axis1.plot(retweets_series, color = "y",label = "retweets")
    axis1.legend(prop = {'size': 20})
    axis2.set_title("sentiment of Trump's tweets")
    axis2.plot(subjectivity_series, color = "b", label = "subjectivity")
    axis2.plot(polarity_series, color = "y", label = "polarity")
    axis2.legend(prop = {'size': 20})
    
    plt.show()
    time_series_figure.savefig("{0}.png".format("time_series"), bbox_inches = 'tight') 
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

tweet_data = pd.read_csv("converted_tweets_sentiment.tsv", sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.

# print(type(tweet_data['date'][2])) # confirms that date is a <class 'pandas.tslib.Timestamp'> 
time_series(tweet_data)
