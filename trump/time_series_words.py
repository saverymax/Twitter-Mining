import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """
    Create a time series plot of word frequencies, as generated in ipynb  
    Would have made this plot iteratively if I had know I was going to do so many words :((((
    """
    
    first_date = '2018-03-18'
    dates = pd.date_range(start = first_date, periods = 11, freq = 'W') 

    china = pd.Series(tweet_dataframe.loc[:, 'china'].values, index = dates)
    korea = pd.Series(tweet_dataframe.loc[:, 'korea'].values, index = dates)
    guns = pd.Series(tweet_dataframe.loc[:, 'guns'].values, index = dates)
    immigration = pd.Series(tweet_dataframe.loc[:, 'immigration'].values, index = dates)
    trade = pd.Series(tweet_dataframe.loc[:, 'trade'].values, index = dates)
    russia = pd.Series(tweet_dataframe.loc[:, 'russia'].values, index = dates)
    wall = pd.Series(tweet_dataframe.loc[:, 'wall'].values, index = dates)
    fake = pd.Series(tweet_dataframe.loc[:, 'fake'].values, index = dates)
    fbi = pd.Series(tweet_dataframe.loc[:, 'fbi'].values, index = dates)
    comey = pd.Series(tweet_dataframe.loc[:, 'comey'].values, index = dates)
    great = pd.Series(tweet_dataframe.loc[:, 'great'].values, index = dates)
   
   
    colors =[
            '#C03028',
            '#F08030',
            '#6890F0',
            '#78C850',
            '#A890F0',
            '#A040A0',
            '#F8D030',
            '#E0C068',
            '#A8A878',
            '#B8A038',
            '#800000',
            ]
     
    time_series_figure, axis1 = plt.subplots(1,1, figsize = (20,10), sharex = True)

    time_series_figure.suptitle("Word frequencies over time", fontsize = 20)
    axis1.set_title("Word use per week", fontsize = 15)
    axis1.set_xlabel('Date', fontsize = 20)
    axis1.set_ylabel('Frequency of terms', fontsize = 20)
    axis1.tick_params(labelsize = 15)
    
               
    axis1.plot(china, color = colors[0], linewidth = 7, label = "China")
    axis1.plot(korea, color = colors[1], linewidth = 7, label = "Korea")
    axis1.plot(guns, color = colors[2], linewidth = 7, label = "guns")
    axis1.plot(immigration, color = colors[3], linewidth = 7,label = "immigration")
    axis1.plot(russia, color = colors[4], linewidth = 7, label = "russia")
    axis1.plot(trade, color = colors[5], linewidth = 7, label = "trade")
    axis1.plot(wall, color = colors[6], linewidth = 7, label = "wall")
    axis1.plot(fbi, color = colors[7], linewidth = 7,label = "fbi")
    axis1.plot(comey, color = colors[8], linewidth = 7,label = "comey")
    axis1.plot(fake, color = colors[9], linewidth = 7,label = "fake")
    axis1.plot(great, color = colors[10], linewidth = 7,label = "great")

    axis1.legend(prop = {'size': 20}, fontsize = 20)
    time_series_figure.savefig("{0}.png".format("time_series_word_frequency"), bbox_inches = 'tight') 
    
    plt.show()
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
os.chdir(path)

tweet_data = pd.read_csv("word_frequencies.tsv", sep = '\t') 

time_series(tweet_data)
