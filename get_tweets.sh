#!/timor/bin/env bash

for senator in $(cat senators_twitter_accounts.txt)
do
	echo $senator
	python get_users_tweets.py $senator 50

	python tweet_analysis.py $senator	
	# call tweet generator for each senator, genearte json of all tweets
	# produce visual for each senator, or combine all tweets into one json
done

