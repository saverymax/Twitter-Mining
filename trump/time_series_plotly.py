import plotly_credentials
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)

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
                            ) # default is a line plot
    polarity_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['polarity'].values, 
                            name = 'Polarity',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) # default is a line plot
    sentiment_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['subjectivity'].values, 
                            name = 'Sentiment',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) # default is a line plot

    # data_1 = [likes_data, retweets_data] # Use these to plot two data sets on one graph
    # data_2 = [polarity_data, sentiment_data] 
    # plot_url = py.plot(data_1)

    fig = tls.make_subplots(rows=2, cols=1, subplot_titles = ("Likes and Retweets", "Polarity and Subjectivity"))
    fig['layout'].update(title="Time series of trumps tweets")
    # fig = go.Figure(data = data, layout = layout) # can use this line for more customization. See below url.
    # https://plot.ly/python/time-series/
    fig.append_trace(retweets_data, 1, 1)
    fig.append_trace(likes_data, 1, 1)
    fig.append_trace(polarity_data, 2, 1)
    fig.append_trace(sentiment_data, 2, 1)
    plot_url = py.plot(fig) 

def normalize_data(tweet_dataframe):
    """Normalize columns in the tweet data, especially since polarity and subjectivity and are two different scales."""

    tweet_dataframe['polarity'] =tweet_dataframe['polarity'].apply(lambda x: (x**2)/x) 
    #(tweet_dataframe['polarity']**2)/tweet_dataframe['polarity']  
    print(tweet_dataframe['polarity'])
    return(tweet_dataframe)

path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

tweet_data = pd.read_csv("converted_tweets_sentiment.tsv", sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.
#tweet_data = normalize_data(tweet_data) # this isn't working because can't do math with zeros
time_series(tweet_data)