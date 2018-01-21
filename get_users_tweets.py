import tweepy
from tweepy import OAuthHandler
import json
import sys
import os
"""
This program generates a json file that contains the specificed number of
tweets from a specified user. If called by get_tweets.sh, the program will generate .json files for each user run through get_tweets.sh. .json files will be named according to user. 

To properly run the script, enter python user_tweet.py screen name for twitter user; number of tweets to grab e.g., POTUS 200 or @POTUS 200

Currently, this file is called by get_tweets.sh
"""

consumer_key = '7GSXtxZvVxgMqc7zQms88Rn1A'
consumer_secret = 'DmiMJPPFbzPc0fTykPl97JIL4J0DeU69hfXrzPvw1vu2xAoYZL'
access_token = '564338092-dOtS6UWrFzLS3WDbA3YuqaEeYKMnCnMCA6kH3dPH'
access_secret = 'gOPv6wJ2xXwJBP4jU6vFpQ99Iyla5rZkLbGzYH29NAS5C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
# Download users tweets

def users_tweets(user,quantity):
    #initialize a list to hold all the tweepy Tweets
    tweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = user).items(int(quantity)):
            tweets.append(tweet._json)
    
    path = '/home/timor/Documents/Git/Twitter-Mining/twitter_data' # Path has to be complete
    os.chdir(path)
    
    # Save a file as .json, that will be processed later
    
    with open(sys.argv[1] + '_twitter_data.json', 'w+') as outfile: 
    
    # Save a file as .json, that will be processed later. 'a' will add to file, w+ will write over existing file, if I want to update. 

         json.dump(tweets, outfile) # .dump dumps into file. .dumps turns dict into str data structure
# ('~/Documents/Git/Twitter-Mining/twitter_data/' 

if __name__ == '__main__':

    #get tweets for username passed at command line. Just = Enter username when calling file
    if len(sys.argv) == 3:
        users_tweets(sys.argv[1],sys.argv[2]) # Element one is the file
    else:
        print("Error: enter one username followed by the number of tweets to grab")
# Add try except to above code

# Used https://github.com/gitlaura/get_tweets/blob/master/get_tweets.py to create script
