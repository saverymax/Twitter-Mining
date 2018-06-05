import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""

    topics = [
            'russia', 
            'immigration', 
            'hubris',
            'korea',
            'secretary_of_state',
            'MS-13',
            'investigation',
            'wall',
            'campaign',
            'fake_news',
            'trade'
            ]

    topics_pass = [
            'immigration',
            'hubris',
            'MS-13',
            'campaign'
            ]

    time_series_figure, axis1 = plt.subplots(1,1, figsize = (20,10), sharex = True)

    # Set date range for later:
    first_date = tweet_dataframe['date'].min()
    dates = pd.date_range(start = first_date, periods = 11, freq = 'W') 
    
    for i, topic in enumerate(topics):
        
        # Some topics aren't very "good", ie the model does a poor job
        if topic in topics_pass:
            continue

        # Set a week column, as I will be counting tweets per week
        tweet_dataframe['week'] = tweet_dataframe['date'].dt.week
        # Iterate through each topic
        tweet_counts = [] 
        topic_dataframe = tweet_dataframe.loc[tweet_dataframe['labels'] == i].copy()

        # Count the tweets per week for given topic
        start = tweet_dataframe['week'].min() 
        stop = tweet_dataframe['week'].max() + 1       
        for i in range(start, stop):
            tweet_counts.append(sum(topic_dataframe['week'] == i))

        # Create a daterange based on tweet dates
        topic_series = pd.Series(tweet_counts, index = dates) 
        # Add plot to figure
        axis1.plot(topic_series, linewidth = 7, label = topic)

    time_series_figure.suptitle("Topic Modeling over time", fontsize = 25)
    axis1.set_title("Topics per week", fontsize = 20)
    axis1.legend(prop = {'size': 20}, fontsize = 20)
    axis1.set_xlabel('Date', fontsize = 20)
    axis1.set_ylabel('Frequency of tweets', fontsize = 20)
    axis1.tick_params(labelsize = 15)

    time_series_figure.savefig("{0}.png".format("time_series_topics"), bbox_inches = 'tight') 
    plt.show()
    plt.close()

path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
os.chdir(path)

tweet_data = pd.read_csv("topic_labels_sentiment_converted_tweets.tsv", sep = '\t', parse_dates = [1]) 

#tweet_data['date'] = pd.to_datetime(tweet_data['date'])
#tweet_data = tweet_data.assign(date=tweet_data.date.dt.round('w'))
#tweet_data.set_index('topic', inplace = True)
time_series(tweet_data)
