from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import argparse
import pandas as pd
import os

def get_parser():
    """
    Set up command line options. In this script, the filename of the tsv to be read must be given. Include file extension.
    Documentation:
    docs.python.org/2/library/argparse.html
    """

    parser = argparse.ArgumentParser(description = "Twitter stream")
    parser.add_argument("--file",
                        dest = "filename",
                        help = "The file to be analyzed")
    return parser


class sentiment_class

    def process_sentiment(self):
        """Analyze sentiment with Textblob and vader libraries. Dataframe must be filtered before this method is called."""

        print("Beginning sentiment analysis")
        # textblob time
        tweet_sentiment = [TextBlob(tweet['filtered_text']).sentiment for index, tweet in self.tweet_dataframe.iterrows()]
        self.tweet_dataframe['polarity'] = [i.polarity for i in tweet_sentiment]

        self.tweet_dataframe['subjectivity'] = [i.subjectivity for i in tweet_sentiment]

        #vader time
        #http://t-redactyl.io/blog/2017/04/applying-sentiment-analysis-with-vader-and-the-twitter-api.html

        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(tweet)
        sentiment = vs['compound']

        self.tweet_dataframe['vader_polarity'] = [analyzer.polarity_scores(i) for i in tweet_sentiment]


    def save_dataframe(self):
        """
        Save the dataframe
        """

        print("Saving...")
        self.tweet_dataframe.to_csv('~/Documents/Git/Twitter-Mining/streaming_tweets/data/{}'.format(self.filename), sep='\t', index = False)
        #self.tweet_dataframe.to_csv('test_5.tsv', sep = '\t', index = False)

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze.
    # make sure to filter dataframe first
    parser = get_parser()
    args = parser.parse_args()

    path = '/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data'
    os.chdir(path)

    tweet_dataframe = pd.read_csv(args.filename, sep='\t')

    analysis = sentiment_class(tweet_dataframe, args.filename)

    analysis.save_dataframe()
    #analysis.process_sentiment()
