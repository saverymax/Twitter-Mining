import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
    investigation = pd.Series(tweet_dataframe.loc['investigation'].values)
    china = pd.Series(tweet_dataframe.loc['china'].values)
    korea = pd.Series(tweet_dataframe.loc['north_korea'].values)
    politics = pd.Series(tweet_dataframe.loc['politics'].values)
    immigration = pd.Series(tweet_dataframe.loc['immigration'].values)

   
    time_series_figure, axis1 = plt.subplots(1,1, figsize = (32,16), sharex = True)

    time_series_figure.suptitle("Topic Modeling over time", fontsize = 20)
    axis1.set_title("Topics per week", fontsize = 15)
    axis1.plot(investigation, color = "b", label = "investigation")
    axis1.plot(china, color = "grey", label = "China")
    axis1.plot(korea, color = "r", label = "North Korea")
    axis1.plot(politics, color = "g", label = "misc. politics")
    axis1.plot(immigration, color = "y", label = "immigration")
    axis1.legend(prop = {'size': 20}, fontsize = 15)
    
    plt.show()
    time_series_figure.savefig("{0}.png".format("time_series_topics"), bbox_inches = 'tight') 
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
os.chdir(path)

tweet_data = pd.read_csv("topic_time_series_revised.tsv", sep = '\t') 

tweet_data.fillna(value = 0, inplace = True)
tweet_data.set_index('topic', inplace = True)
time_series(tweet_data)
