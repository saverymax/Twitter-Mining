import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets"""
   
    likes_plt = pd.Series(data = tweet_dataframe['likes'].values, index = tweet_dataframe['date'])
    retweets_plot = pd.Series(data=tweet_dataframe['retweets'].values, index=tweet_dataframe['date'])
    likes_plt.plot(figsize = (16,4), color = 'g', label = 'Likes', legend = True)
    retweets_plot.plot(figsize = (16,4), color = 'r', label = 'retweets', legend = True)
    
    plt.savefig("{0}.png".format("time_series"), bbox_inches = 'tight') 
    plt.show()
    plt.close()
    # seaborn implementation
    #retweet_plot = sns.tsplot(time = tweet_dataframe['date'], value = tweet_dataframe['retweets'], data = tweet_dataframe)


path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

tweet_data = pd.read_csv("converted_tweets.tsv", sep = '\t', parse_dates=[1]) 

# print(type(tweet_data['date'][1])) # confirms that date is a <class 'pandas.tslib.Timestamp'> 
time_series(tweet_data)
