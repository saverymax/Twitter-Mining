import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import argparse
import string
import config
import json 
import time

"""This file will generate a twitter stream of a term or set of terms, for a given period of time, as specified in command line. http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html was used as documentation.

To run, see sample below:
--term dog cat pig #diggity --time 180
This will search for all terms for 3 minutes. 
"""

def get_parser():
    """
    Set up command line options. In this program, time that stream will run and terms that will be searched for are used as command line options. As many terms as desired can be passed in command line. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Twitter stream") 
    parser.add_argument("--terms", 
                        dest = "terms", 
                        nargs='+',
                        help = "Terms to search via twitter")
    parser.add_argument("--time",
                        dest = "time",
                        type = int,
                        help = "Time to stream tweets",
                        default = 20)
    return parser

class MyStreamListener(tweepy.StreamListener):
    """The class that will deal with all streaming data. Inherits from class defined by tweepy
    Documentation:
    https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
    """

    def __init__(self, time_limit, start_time, term_list):
        """Initiate instance of tweet stream, setting timie_limit of the stream"""
        print("init") 
        self.time_limit = time_limit 
        self.start_time = start_time
        self.term_list = "_".join(term_list)

    def on_status(self, status):
        """Called when a new status arrives i.e., a new tweet that matches specified terms"""

        print("Saving...\n")
        
        with open("/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/streaming_{0}.jsonl".format(self.term_list),'a') as outfile:
            outfile.write(json.dumps(status) + "\n")

        return True 

    def on_data(self, data):
        """Called when raw data is received from connection."""
        
        while (time.time() - self.start_time) < self.time_limit:
            data = json.loads(data) 
            
            try:
                # If statements are necessary to deal with deleted tweets and tweet limit that prevent tweet from being added to jsonl
                if "delete" in data:
                    print("deleted tweet found")
                    pass

                elif 'limit' in data:
                    print("limit in data found")
                    pass

                # All this to get full text from retweets. The only problem is that I lose the RT @user info, which is annoying 

                elif 'retweeted_status' in data:
                    if 'extended_tweet' in data['retweeted_status']:
                        tweet = data['retweeted_status']['extended_tweet']['full_text']
                        print("Extended retweet:", tweet, "\n")
                        self.on_status(data) 
                    # If retweet isn't long enough to need extended text
                    else:
                        tweet = data['retweeted_status']['text']
                        print("Retweet", tweet, "\n")
                        self.on_status(data) 

                elif "extended_tweet" in data:
                    tweet = data['extended_tweet']['full_text']
                    print("Extended tweet", tweet, "\n")
                    self.on_status(data) 

                # Need this next if statement to deal with tweets that aren't long enough to need extended text.
                elif "text" in data:
                    print("Just 'text' of tweet okay?")
                    tweet = data['text']
                    print(tweet, "\n")
                    self.on_status(data) 

                else:
                    tweet = data
                    print("Tweet that's something I don't understand")
                    print(tweet, "\n")

            except BaseException as e:
                print("Error in method on_data: {}".format(e))
                time.sleep(1) 
            
            except tweepy.TweepError as e:
                print("Tweepy error:".format(e))
                time.sleep(1)
            
            return True # Return true to keep stream flowing

        return False # Return false to end stream
    
    def on_exception(self, exception):
        """Handle error: connection broken: IncompleteRead(0 bytes read, 512 more expected)"""
        # ref: https://github.com/tweepy/tweepy/issues/650
        print(exception)
        return


if __name__== '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    #api = tweepy.API(auth)
    # try:
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    start_time = time.time()

    twitter_scraper = MyStreamListener(time_limit = args.time, start_time = start_time, term_list = args.terms) # Create the instance and set the time_limit. 
    tweet_stream = tweepy.Stream(auth = api.auth, listener = twitter_scraper, tweet_mode= "extended")
    tweet_stream.filter(track=[",".join(args.terms)]) # Filter searches for all words in given list, and as args.terms is in a list, I have to unpack it first.
    tweet_stream.disconnect() #disconnect the stream and stop streaming
