import dash
import dash_core_components as dcc
import dash_html_components as html
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


def time_series(path):
    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""
    
    tweet_dataframe = pd.read_csv('{}sentiment_topic_labels_tweets.tsv'.format(path), sep = '\t', parse_dates=[0]) # Neccessary to parse_dates to put in format that can be read and plotted.
    # Do some date revising. Round to day
    tweet_dataframe['date'] = pd.to_datetime(tweet_dataframe['date'])
    #tweet_data = tweet_data.assign(date=tweet_data.date.dt.round('D'))

    # create individual plotly plotting objects. These will be added to subplots below

    tweet_dataframe['custom_text'] = tweet_dataframe[['username', 'text']].apply(lambda x: '<br />'.join(x), axis=1).copy() 
    retweets_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['retweets'].values, 
                            name = 'Retweets',
                            mode = 'markers', 
                            line = dict(color = '#3498db'),
                            text = tweet_dataframe['custom_text'],
                            hoverinfo = 'text'
                            ) # default is a line plot
    # For senitment analysis see description given by Tweepy documentation:
    # "The polarity (positivity and negativity) score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective."
    
    likes_data = go.Scatter(
                            x = tweet_dataframe['date'], 
                            y = tweet_dataframe['likes'].values, 
                            name = 'Likes',
                            mode = 'markers',
                            line = dict(color = '#27ae60'),
                            text = tweet_dataframe['text']) 


    data = [retweets_data, likes_data] # Use these to plot two data sets on one graph
    
    empty_axis = dict(zeroline=False, showaxeslabels=False, showticklabels=False, title='')
    layout = dict(
            scene = dict(
                    xaxis = empty_axis,
                    yaxis = empty_axis,
                    ),
                hovermode = "closest",
                title = "Likes and retweet frequency",
                showlegend = True)
    
    return data, layout

def average_data(column_name):
    """Normalize columns in the tweet data, particularly because polarity and subjectivity and are on two different scales."""

    normalized_data = pd.Series(scale(column_name))
    return(normalized_data)

"""    
path = '/home/timor/Documents/Git/search_bot/data/'
os.chdir(path)

tweet_data = pd.read_csv('sentiment_topic_labels_tweets.tsv', sep = '\t', parse_dates=[0]) # Neccessary to parse_dates to put in format that can be read and plotted.
# Do some date revising. Round to day
tweet_data['date'] = pd.to_datetime(tweet_data['date'])
#tweet_data = tweet_data.assign(date=tweet_data.date.dt.round('D'))

plot_list, layout = time_series(tweet_data)


app = dash.Dash()

app.layout = html.Div(children = [
    html.H1(children = 'Topic model of twitter'),
    html.Div(children = '''tweets that included the word'''),
    dcc.Graph(
        id = 'time series of retweets',
        figure = {
            'data': [plot_list[0]],
            'layout': layout
            }),
    dcc.Graph(
        id = 'time series of sentiment',
        figure = {
            'data': [plot_list[1]],
            'layout': layout
            })
        ])

if __name__ == "__main__":

    app.run_server()
"""
