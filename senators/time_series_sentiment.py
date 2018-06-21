import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt 
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.offline as offline_plot
import os
import pickle

def time_series(path):

    """Using data from pandas dataframe, create a time series plot of retweets, likes, polarity and subjectivity"""

    tweet_dataframe = pd.read_csv("data/sentiment_topic_labels_tweets.tsv", sep = '\t', parse_dates = [0]) 

    with open('topics.pickle', 'rb') as f:
        topics = pickle.load(f)
    topic_plots = []

    for i, topic in enumerate(topics):
        
        # Iterate through each topic
        topic_dataframe = tweet_dataframe.loc[tweet_dataframe['labels'] == i].copy()
        date_range = tweet_dataframe['date'].max() - timedelta(days = 5)
        topic_dataframe['custom_text'] = topic_dataframe[['username', 'text']].apply(lambda x: '<br />'.join(x), axis=1) 

        topic_plot = go.Scatter(
                x = topic_dataframe['date'].loc[topic_dataframe['date'] > date_range],
                y = topic_dataframe['vader_polarity'],
                name = topic,
                mode = 'markers',
                hoverinfo = 'text',
                #text = topic_dataframe['text'],
                hovertext = topic_dataframe['custom_text']
                )#, topic_dataframe['username']])
        
        topic_plots.append(topic_plot)
    
 
    empty_axis = dict(zeroline=False, showaxeslabels=False, showticklabels=False, title='')
    layout = dict(
            scene = dict(
                    xaxis = empty_axis, 
                    yaxis = empty_axis,
                    ),
                hovermode = "closest",
                title = "Sentiment per topic, over time",
                showlegend = True)

    return topic_plots, layout    

if __name__ == "__main__":

    path = '/home/timor/Documents/Git/Twitter-Mining/senators/'


    #tweet_data['date'] = pd.to_datetime(tweet_data['date'])
    #tweet_data = tweet_data.assign(date=tweet_data.date.dt.round('w'))
    #tweet_data.set_index('topic', inplace = True)
    plot_list, layout = time_series(path)
    fig = dict(data=plot_list, layout=layout)
    offline_plot.plot(fig, filename='{}data/sentiment_time_series.html'.format(path), auto_open = True)


