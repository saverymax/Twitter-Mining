import plotly_credentials # local file with my plotly login
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import scale
import os


"""
Script in which time series of President Trump's tweets is generated. Two plots are produced: One comparing frequency of retweets and likes, another comparing subjectivity and polarity. The polarity metric describes the positive and negative content used in the text of the tweets. 

The plots can be found at https://saverymax.github.io/Twitter-Mining/Trump_time_series
"""


def time_series(tweet_dataframe):
    """
    Using data from pandas dataframe, create a time series plot of the president's retweets, likes, polarity and subjectivity
    See https://plot.ly/python/time-series/ for documentation.
    """
   
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password) # Login to plotly

    # create individual plotly plotting objects. These will be added to subplots below
    likes_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['likes'].values, 
                            name = 'Likes',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']
                            ) # default is a line plot

    retweets_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['retweets'].values, 
                            name = 'Retweets',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']
                            )

    # For senitment analysis see description given by Tweepy documentation:
    # "The polarity (positivity and negativity) score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective."
    polarity_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['polarity'].values, 
                            name = 'Polarity',
                            mode = 'markers',
                            text = tweet_dataframe['filtered_text']) 

    sentiment_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['subjectivity'].values, 
                            name = 'Sentiment',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) 

    fig = tls.make_subplots(rows=2, cols=1, subplot_titles = ('Likes and Retweets', 'Polarity and Subjectivity'))
    fig['layout'].update(title='Time series of President Trumps tweets')
    fig['layout']['xaxis1'].update(title='Date')
    fig['layout']['yaxis1'].update(title='Likes and Retweet Frequency')
    fig['layout']['xaxis2'].update(title='Date')
    fig['layout']['yaxis2'].update(title='Polarity and Subjectivity Score')
    


    fig.append_trace(retweets_data, 1, 1) # 1,1 refers to location of subplot in fig object
    fig.append_trace(likes_data, 1, 1)
    fig.append_trace(polarity_data, 2, 1)
    fig.append_trace(sentiment_data, 2, 1)
    plot_url = py.plot(fig) 

def normalize_data(column_name):
    """Normalize columns in the tweet data, particularly because polarity and subjectivity and are on two different scales."""

    normalized_data = pd.Series(scale(column_name))
    return(normalized_data)

path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

tweet_data = pd.read_csv('converted_tweets_sentiment.tsv', sep = '\t', parse_dates=[2]) # Neccessary to parse_dates into format that can be read and plotted.

tweet_data['polarity'] = normalize_data(tweet_data['polarity'])
tweet_data['subjectivity'] = normalize_data(tweet_data['subjectivity'])
time_series(tweet_data)

