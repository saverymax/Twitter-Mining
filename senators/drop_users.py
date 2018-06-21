from tweepy import OAuthHandler
import time
import config
import pandas as pd
import tweepy

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

path = '~/Documents/Git/Twitter-Mining/senators/'

congress_handles = pd.read_csv('{}congress_handles.tsv'.format(path), sep = '\t')

for handle in congress_handles['handles']: 

    try:
        following_info = api.show_friendship(source_screen_name = 'mysavorytweets', target_screen_name = handle)

    except tweepy.TweepError as e:
        print("Error:", e, handle)

        drop = input("drop user?")
        if drop == 'y':
        
            congress_handles_edit = congress_handles[congress_handles['handles'] != handle]

            congress_handles_edit.to_csv('{}congress_handles.tsv'.format(path), sep='\t', index = False)

        continue
