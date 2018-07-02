import json
import plotly.offline as offline_plot
import plotly.graph_objs as go
from plotly.offline import plot_mpl
import plotly.tools as tls
import matplotlib.pyplot as plt
import argparse

"""
Useful script to visualize frequency of types of tweets: tweets, replies, and retweets
Just run python tweet_frequency.py
Currently plots with plotly. I also want matplotlib
"""

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


class frequency_class():
    """
    Class to count retweets, replies, and tweets
    """

    def __init__(self, directory):
        """
        Initiate tweet counter
        """
    
        self.retweet_cnt = 0
        self.reply_cnt = 0
        self.tweet_cnt = 0
        self.directory = directory
 
    def frequency_counter(self):
        """
        Count the frequencies of tweet types
        """

        with open('data/{}/stream.jsonl'.format(self.directory), 'r') as infile:
           
            for line in infile:
                tweet = json.loads(line)

                try:
                    if 'retweeted_status' in tweet:
                        #print("retweet?\n", tweet, "\n")
                        self.retweet_cnt += 1

                    elif tweet['in_reply_to_screen_name'] != None:

                        #print("reply?\n", tweet, "\n")
                        self.reply_cnt += 1

                    else:
                        #print("tweet?\n", tweet['in_reply_to_screen_name'], "\n")
                        self.tweet_cnt += 1

                except KeyError as e:
                    print("Reassess your life's priorities\n")
                    raise

    def mpl_visualize_frequencies(self):
        """
        Plot the frequencies with mpl
        """
 
        labels = ['retweets', 'replies', 'tweets']
        frequencies = [self.retweet_cnt, self.reply_cnt, self.tweet_cnt]
        total = sum(frequencies)
        explode = (.1, .1, .1)
        plt.pie(
                frequencies, 
                explode = explode, 
                labels = labels,
                autopct = lambda p: '{:.0f}'.format(p * total / 100),
                )
        plt.savefig('data/{}/tweet_frequencies.png'.format(self.directory))

    def plotly_visualize_frequencies(self):
        """
        Plot the frequencies with plotly. 
        """
        
        labels = ['retweets', 'replies', 'tweets']
        frequencies = [self.retweet_cnt, self.reply_cnt, self.tweet_cnt]
        trace = go.Pie(labels = labels, values = frequencies)

        offline_plot.plot(
                [trace], 
                filename='data/{}/tweet_frequencies.html'.format(self.directory), 
                auto_open = False,
                )

if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    counter = frequency_class(args.directory)
    counter.frequency_counter()
    counter.plotly_visualize_frequencies()
    counter.mpl_visualize_frequencies()
