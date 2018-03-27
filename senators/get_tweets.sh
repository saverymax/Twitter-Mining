#!/bin/sh

for senator in $(cat senators_twitter_accounts.txt)
do
	echo $senator
	python get_users_tweets_jsonl.py $senator 100 
done

python tweet_analysis_of_streaming_data.py 
	# call tweet generator for each senator, genearte json of all tweets
	# produce visual for each senator, or combine all tweets into one json

# Note: I modified this so as to generate one graph of all senators tweets. to modify it so that graphs of individual senators tweets are displayed the following changes must be implemented:
        # python get_users_tweets.py $senator
	# python tweet_analysis.py $senator
