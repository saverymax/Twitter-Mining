import plotly_credentials # private file with my plotly login
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import argparse
from sklearn.preprocessing import scale

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
   
    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)

    # create individual plotly plotting objects. These will be added to subplots below
    likes_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['likes'].values, 
                            name = 'Likes',
                            mode = 'markers', 
                            text = tweet_dataframe['text']
                            ) # default is a line plot
    
    retweets_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['retweets'].values, 
                            name = 'Retweets',
                            mode = 'markers', 
                            text = tweet_dataframe['text']
                            ) # default is a line plot
    # For senitment analysis see description given by Tweepy documentation:
    # "The polarity (positivity and negativity) score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective."
    
    polarity_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['polarity'].values, 
                            name = 'Polarity',
                            mode = 'markers',
                            text = tweet_dataframe['text']) 

    subjectivity_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['subjectivity'].values, 
                            name = 'Subjectivity',
                            mode = 'markers', 
                            text = tweet_dataframe['text']) 
    

    # data_1 = [likes_data, retweets_data] # Use these to plot two data sets on one graph
    # data_2 = [polarity_data, sentiment_data] 
    # plot_url = py.plot(data_1)

    fig = tls.make_subplots(rows=2, cols=1, subplot_titles = ('Likes and Retweets', 'Polarity and Subjectivity'))
    fig['layout'].update(title='Time series of tweets')
    fig['layout']['xaxis1'].update(title='Date')
    fig['layout']['yaxis1'].update(title='Likes and Retweet Frequency')
    fig['layout']['xaxis2'].update(title='Date')
    fig['layout']['yaxis2'].update(title='Polarity and Subjectivity Score')

    # fig = go.Figure(data = data, layout = layout) # can use this line for more customization. See below url.
    # https://plot.ly/python/time-series/

    fig['layout'].update(title="Time series of trumps tweets", hovermode = 'closest')
    # fig = go.Figure(data = data, layout = layout) # can use this line for more customization. See below url.
    # https://plot.ly/python/time-series/
    fig.append_trace(retweets_data, 1, 1)
    fig.append_trace(likes_data, 1, 1)
    fig.append_trace(polarity_data, 2, 1)
    fig.append_trace(subjectivity_data, 2, 1)

    plotly.offline.plot(fig, filename='march-may_trump_series.html')
    
    #plot_url = py.plot(fig) 

def normalize_data(column_name):
    """Normalize columns in the tweet data, particularly because polarity and subjectivity and are on two different scales."""

    normalized_data = pd.Series(scale(column_name))
    return(normalized_data)

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
    
    path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
    os.chdir(path)

    tweet_data = pd.read_csv(args.filename, sep = '\t', parse_dates=[2]) # Neccessary to parse_dates to put in format that can be read and plotted.
    # Do some date revising. Round to day
    tweet_data['date'] = pd.to_datetime(tweet_data['date'])
#    tweet_data = tweet_data.assign(date=tweet_data.date.dt.round('H'))

    tweet_data['polarity'] = normalize_data(tweet_data['polarity'])
    tweet_data['subjectivity'] = normalize_data(tweet_data['subjectivity'])
    time_series(tweet_data)
