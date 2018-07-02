from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import argparse
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from textblob import TextBlob
import pandas as pd
import os


def get_parser():
    """
    Set up command line options. The filename of the jsonl to be read must be given. Include file extension in the path given in the command line. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Modeling topics from twitter stream data") 

    parser.add_argument("--dir", 
                        dest = "directory", 
                        help = "The directory to save the figures.")
    
    return parser

class sentiment_class():

    def __init__(self, directory):
        """
        Initiate class to process sentiment
        """
    
        tweet_dataframe = pd.read_csv("data/{}/reduced_dataframe_tsne_labels.tsv".format(directory), sep='\t')

        self.tweet_dataframe = tweet_dataframe
        self.directory = directory

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

        topic_plot = ax.boxplot(data, patch_artist = True, vert = False)# notch = True, bootstrap = 1000)
        
        for box, color in zip(topic_plot['boxes'], colors):
            box.set_facecolor(color)
        #ax.set_frame_on(False)
        ax.set_title("Sentiment scores for each topic")

        ax.set_ylabel('topics')

        ax.set_xlabel('sentiment score')
        ax.set_yticklabels((topics))
        fig.savefig('data/{}/sentiment_boxplot.png'.format(self.directory), bbox_inches = 'tight')
        

    def save_dataframe(self):
        """
        Save the dataframe
        """

        print("Saving dataframe with sentiment...")
        self.tweet_dataframe.to_csv('data/{}/sentiment_topic_labels_tweets.tsv'.format(self.directory), sep='\t', index = False)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    with open("topics.pickle", 'rb') as f:
        topics = pickle.load(f)
    
    analysis = sentiment_class(args.directory)
    analysis.process_sentiment()
    analysis.visualize(topics)
    analysis.save_dataframe()




