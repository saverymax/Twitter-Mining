import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
    
    first_date = '2018-03-18'
    dates = pd.date_range(start = first_date, periods = 11, freq = 'W') 

    #investigation = pd.Series(tweet_dataframe.loc['investigation'].values)
    china = pd.Series(tweet_dataframe.loc[:, 'china'].values, index = dates)
    korea = pd.Series(tweet_dataframe.loc[:, 'korea'].values, index = dates)
    guns = pd.Series(tweet_dataframe.loc[:, 'guns'].values, index = dates)
    immigration = pd.Series(tweet_dataframe.loc[:, 'immigration'].values, index = dates)
   
    time_series_figure, axis1 = plt.subplots(1,1, figsize = (20,10), sharex = True)

    time_series_figure.suptitle("Word frequencies over time", fontsize = 20)
    axis1.set_title("Word use per week", fontsize = 15)
    axis1.set_xlabel('Date', fontsize = 20)
    axis1.set_ylabel('Frequency of terms', fontsize = 20)
    axis1.tick_params(labelsize = 15)
    
    #axis1.plot(investigation, color = "b", label = "investigation")
    axis1.plot(china, color = "grey", linewidth = 7, label = "China")
    axis1.plot(korea, color = "r", linewidth = 7, label = "Korea")
    axis1.plot(guns, color = "g", linewidth = 7, label = "guns")
    axis1.plot(immigration, color = "y", linewidth = 7,label = "immigration")
    
    axis1.legend(prop = {'size': 20}, fontsize = 20)
    time_series_figure.savefig("{0}.png".format("time_series_word_frequency"), bbox_inches = 'tight') 
    
    plt.show()
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
os.chdir(path)

tweet_data = pd.read_csv("word_frequencies.tsv", sep = '\t') 

time_series(tweet_data)
