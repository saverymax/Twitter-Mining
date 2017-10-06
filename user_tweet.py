import tweepy
from tweepy import OAuthHandler
import json
import sys

"""
This program generates a json file that contains the specificed number of
tweets from a specified user. To properly run the script,
enter python user_tweet.py screen name for twitter user; number of tweets to grab e.g., POTUS 200
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

    # Save a file as .json, that will be processed later
    with open('user_data.json', 'a') as outfile: # Save a file as .json, that will be processed later
        json.dump(tweets, outfile) # .dump dumps into file. .dumps turns dict into str data structure

if __name__ == '__main__':

    #get tweets for username passed at command line. Just = Enter username when calling file
    if len(sys.argv) == 3:
        users_tweets(sys.argv[1],sys.argv[2]) # Element one is the file
    else:
        print("Error: enter one username followed by the number of tweets to grab")

    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)
#used https://github.com/gitlaura/get_tweets/blob/master/get_tweets.py
#for creating script
