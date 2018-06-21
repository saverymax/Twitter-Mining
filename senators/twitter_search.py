import time
import json
import os
import tweepy
from tweepy import OAuthHandler
import config

"""
Script to get the tweets from each user
"""

def search_handler(tweepy_cursor):
    """
    Handle the searching limits:
    """
    while True:
        try:
            yield tweepy_cursor.next()
        
        except tweepy.RateLimitError as e:
            print("Error in search limit:", e)
            time.sleep(60 * 15)

        except tweepy.TweepError as e:
            print("Tweepy error in search script. Might be 429 problem:", e)
            time.sleep(15 * 60)
            continue

        except StopIteration:
            raise

def get_tweets(handle, quantity):
    """
    Get tweets based on search term
    """
 
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
 
    tweepy_cursor = tweepy.Cursor(api.user_timeline,
                                    screen_name = handle,
                                    tweet_mode = 'extended').items(quantity)
    
    for status in search_handler(tweepy_cursor): 
        with open('data/search.jsonl', 'a') as outfile:
            outfile.write(json.dumps(status._json)+"\n") # the .__json method is a method of the Status class
