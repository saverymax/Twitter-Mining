<<<<<<< HEAD
import plotly_credentials # private file with my plotly login
=======
import plotly_credentials
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
<<<<<<< HEAD
from sklearn.preprocessing import scale
import os
import argparse


"""
Script in which time series of tweets is generated. Two plots are produced: One comparing frequency of retweets and likes, another comparing subjectivity and polarity. The polarity metric describes the positive and negative content used in the text of the tweets. 

The plots can be found at https://saverymax.github.io/Twitter-Mining/
"""

def get_parser():
    """
    Set up command line options. In this script, the filename of the jsonl to be read must be given. Include file extension. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Twitter stream") 
    parser.add_argument("--file", 
                        dest = "filename", 
                        help = "The file to be analyzed")
    return parser

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
<<<<<<< HEAD
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)
=======
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password) # Login to plotly
=======
import os

def time_series(tweet_dataframe):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
   
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd

    # create individual plotly plotting objects. These will be added to subplots below
    likes_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['likes'].values, 
                            name = 'Likes',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']
                            ) # default is a line plot
<<<<<<< HEAD

=======
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
    retweets_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['retweets'].values, 
                            name = 'Retweets',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']
<<<<<<< HEAD
                            )

    # For senitment analysis see description given by Tweepy documentation:
    # "The polarity (positivity and negativity) score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective."
<<<<<<< HEAD
    
=======
=======
                            ) # default is a line plot
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd
    polarity_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['polarity'].values, 
                            name = 'Polarity',
<<<<<<< HEAD
                            mode = 'markers',
                            text = tweet_dataframe['filtered_text']) 

    sentiment_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['subjectivity'].values, 
                            name = 'Subjectivity',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) 
<<<<<<< HEAD
    
=======
=======
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) # default is a line plot
    sentiment_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['subjectivity'].values, 
                            name = 'Sentiment',
                            mode = 'markers', 
                            text = tweet_dataframe['filtered_text']) # default is a line plot
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd

    # data_1 = [likes_data, retweets_data] # Use these to plot two data sets on one graph
    # data_2 = [polarity_data, sentiment_data] 
    # plot_url = py.plot(data_1)

<<<<<<< HEAD
    fig = tls.make_subplots(rows=2, cols=1, subplot_titles = ('Likes and Retweets', 'Polarity and Subjectivity'))
    fig['layout'].update(title='Time series of tweets')
    fig['layout']['xaxis1'].update(title='Date')
    fig['layout']['yaxis1'].update(title='Likes and Retweet Frequency')
    fig['layout']['xaxis2'].update(title='Date')
    fig['layout']['yaxis2'].update(title='Polarity and Subjectivity Score')

    # fig = go.Figure(data = data, layout = layout) # can use this line for more customization. See below url.
    # https://plot.ly/python/time-series/

<<<<<<< HEAD
    fig.append_trace(retweets_data, 1, 1)
=======
    fig.append_trace(retweets_data, 1, 1) # 1,1 refers to location of subplot in fig object
=======
    fig = tls.make_subplots(rows=2, cols=1, subplot_titles = ("Likes and Retweets", "Polarity and Subjectivity"))
    fig['layout'].update(title="Time series of trumps tweets")
    # fig = go.Figure(data = data, layout = layout) # can use this line for more customization. See below url.
    # https://plot.ly/python/time-series/
    fig.append_trace(retweets_data, 1, 1)
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd
    fig.append_trace(likes_data, 1, 1)
    fig.append_trace(polarity_data, 2, 1)
    fig.append_trace(sentiment_data, 2, 1)
    plot_url = py.plot(fig) 

<<<<<<< HEAD
def normalize_data(column_name):
    """Normalize columns in the tweet data, particularly because polarity and subjectivity and are on two different scales."""

    normalized_data = pd.Series(scale(column_name))
    return(normalized_data)
=======
def normalize_data(tweet_dataframe):
    """Normalize columns in the tweet data, especially since polarity and subjectivity and are two different scales."""

    tweet_dataframe['polarity'] =tweet_dataframe['polarity'].apply(lambda x: (x**2)/x) 
    #(tweet_dataframe['polarity']**2)/tweet_dataframe['polarity']  
    print(tweet_dataframe['polarity'])
    return(tweet_dataframe)
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134

<<<<<<< HEAD
if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
    
    path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
    os.chdir(path)
=======
path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
os.chdir(path)

<<<<<<< HEAD
tweet_data = pd.read_csv('converted_tweets_sentiment.tsv', sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd

    tweet_data = pd.read_csv(args.filename, sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.

<<<<<<< HEAD
    tweet_data['polarity'] = normalize_data(tweet_data['polarity'])
    tweet_data['subjectivity'] = normalize_data(tweet_data['subjectivity'])
    time_series(tweet_data)
=======
=======
tweet_data = pd.read_csv("converted_tweets_sentiment.tsv", sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.
#tweet_data = normalize_data(tweet_data) # this isn't working because can't do math with zeros
time_series(tweet_data)
>>>>>>> 0755d4310b0bb7aa18eb4bbf5b1288e615c9e134
>>>>>>> 8670af71ac5e97086f60fb91e67cc24895b178fd
