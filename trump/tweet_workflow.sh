#!/bin/sh

echo 'Collecting and visualzing trumps tweets'
python get_trumps_tweets.py realDonaldTrump 500 
python analyze_trumps_tweets.py 
python sentiment_analysis.py --file converted_tweets.tsv
python time_series.py
