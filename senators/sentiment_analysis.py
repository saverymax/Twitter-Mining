from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from textblob import TextBlob
import pandas as pd
import os
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.offline as offline_plot
import pickle


class sentiment_class():

    def __init__(self, path):
        """
        Initiate class to process sentiment
        """
    
        tweet_dataframe = pd.read_csv("{}sentiment_topic_labels_tweets.tsv".format(path), sep='\t')

        self.tweet_dataframe = tweet_dataframe
        self.path = path

    def process_sentiment(self):
        """Analyze sentiment with Textblob and vader libraries. Dataframe must be filtered before this method is called."""


        print("Beginning sentiment analysis")
        # textblob time
        #tweet_sentiment = [TextBlob(tweet['filtered_text']).sentiment for index, tweet in self.tweet_dataframe.iterrows()]
        #self.tweet_dataframe['polarity'] = [i.polarity for i in tweet_sentiment]
        #self.tweet_dataframe['subjectivity'] = [i.subjectivity for i in tweet_sentiment]

        #vader time
        #http://t-redactyl.io/blog/2017/04/applying-sentiment-analysis-with-vader-and-the-twitter-api.html
        sentiment = []

        analyzer = SentimentIntensityAnalyzer()

        for tweet in self.tweet_dataframe['filtered_text']:
            vs = analyzer.polarity_scores(tweet)
            sentiment.append(vs['compound'])

        self.tweet_dataframe['vader_polarity'] = pd.Series(sentiment)
    
    def visualize(self, topics):
        """
        Generate boxplots of sentiment per topic
        """

        topic_set = set(pd.Series(self.tweet_dataframe['labels']))
        gradient = np.linspace(0, 1, len(topic_set))
        colors = plt.cm.tab20(gradient)
        #colors = [plt.cm.Pastel2(gradient[i]) for i in topic_set]
        box_style = dict(facecolor = colors)

        fig, ax = plt.subplots()

        data = []
        for i in topic_set:
            topic_sentiment = pd.Series(self.tweet_dataframe.loc[self.tweet_dataframe['labels'] == i, 'vader_polarity'])
            data.append(topic_sentiment)

        topic_plot = ax.boxplot(data, patch_artist = True, vert = False)#, notch = True)
        
        for box, color in zip(topic_plot['boxes'], colors):
            box.set_facecolor(color)
        #ax.set_frame_on(False)
        ax.set_title("Sentiment scores for each topic")

        ax.set_ylabel('topics')

        ax.set_xlabel('sentiment score')
        ax.set_yticklabels((topics))
        fig.savefig('data/sentiment_boxplot.png', bbox_inches = 'tight')
        
    def visualize_plotly(self, topics):
        """ 
        Generate interactive boxplot with plotly
        https://plot.ly/python/reference/#box
        """
                    
        df_palette = pd.DataFrame([
                [0, '#C03028'],
                [1, '#F08030'],
                [2, '#6890F0'],
                [3, '#78C850'],
                [4, '#A890F0'],
                [5, '#B22222'],
                [6, '#F8D030'],
                [7, '#D3D3D3'],
                [8, '#F85888'],
                [9, '#7FFFD4']])
                #[10, '#98D8D8']])
                
                #[11, '#A8B820'],
                #[12, '#7038F8'],
                #[13, '#705898'],
                #[14, '#705848'],
                #[15, '#B8B8D0'],
                #[16, '#A8A878'],
                #[17, '#EE99AC']])

        df_palette.columns = ['labels', 'typecolor']
        self.tweet_dataframe.merge(df_palette, on = 'labels')

        #Divide up the tsne data

        plot_list = []

        for idx, (label, color) in df_palette.iterrows():

            df_filter = self.tweet_dataframe[self.tweet_dataframe['labels'] == label]
            
            df_filter['custom_text'] = df_filter[['username', 'text']].apply('<br />'.join, axis = 1) 
            sentiment_boxplot = go.Box(
                    x = df_filter['vader_polarity'],
                    name = "{}".format(topics[label]),
                    #text = pd.Series(self.tweet_dataframe['text']),
                    boxmean = True,
                    jitter = .5,
                    boxpoints = 'all',
                    hoverinfo = 'x+text',
                    text = df_filter['custom_text'],
                    marker = dict(color = color) 
                    )
            plot_list.append(sentiment_boxplot) 

        # Override plotly 
        axis_layout = dict(zeroline=False, showaxeslabels=False, autotick = True, ticks = '', showticklabels=False, title='')

        layout = go.Layout(
                    yaxis = axis_layout,
                    hovermode = "closest",
                    title = "Sentiment distribution per topic",
                    showlegend = True)

        fig = dict(data=plot_list, layout=layout)
        #plot_url = py.plot(fig)
        offline_plot.plot(fig, filename='data/sentiment_boxplot.html', auto_open = False)

        return plot_list, layout

    def save_dataframe(self):
        """
        Save the dataframe
        """

        print("Saving dataframe with sentiment...")
        self.tweet_dataframe.to_csv('{}sentiment_topic_labels_tweets.tsv'.format(self.path), sep='\t', index = False)

if __name__ == "__main__":

    with open('topics.pickle', 'rb') as f:
        topics = pickle.load(f)
 
    path = '~/Documents/Git/Twitter-Mining/senators/'
    sentiment_instance = sentiment_class(path)
    sentiment_instance.visualize_plotly(topics)

