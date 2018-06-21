import plotly_tsne
import os
import twitter_search
import json_to_tsv
import tweet_cleaner
import sentiment_analysis
import topic_modeling
import time
import pandas as pd
import time_series_plotly
import time_series_sentiment
import pickle

"""
This program collects and analyzes tweets from all members of congress.
"""

def run_pipeline():
    """
    Run the pipeline. To be called from congress_app.py
    """

    path = '~/Documents/Git/Twitter-Mining/senators/data/' # Path has to be complete

    congress_handles = pd.read_csv('~/Documents/Git/Twitter-Mining/senators/congress_handles.tsv', sep = '\t')

    congress_handles = pd.read_csv('congress_handles.tsv', sep = '\t')
    quantity = 2 

    # Create new jsonl for senators tweets
    # Handles errors within script
    with open('data/search.jsonl', 'w') as outfile:
        print("Create new json file\n")

    for handle in congress_handles['handles']:
        print(handle)

        twitter_search.get_tweets(handle, quantity)

    # Do the analysis
    try:
        # Convert to tsv
        convert_jsonl = json_to_tsv.tweetflow(path)
        convert_jsonl.read_tweets()

        # Tweet cleaning
        clean_tweets = tweet_cleaner.process_tweet(path)
        clean_tweets.filter_tweet()
        clean_tweets.lemmatization()
        clean_tweets.save_dataframe()

        # Perform analysis with NMF or LDA. Would be nice to choose from command line.
        n_topics = 10 
        model = topic_modeling.modeling(path)
         
        transformed_data_lda, topics = model.lda_analysis(n_topics)
        model.run_tsne(transformed_data_lda) 
            
        # If I want to plot model with only tweets most likely to be in a topic:
        model.drop_tweets(transformed_data_lda) 

        # Only run if saving tsne data is necessary 
        model.save_dataframe()
        with open('topics.pickle', 'wb') as f:
            pickle.dump(topics, f)


        # Visualization
        model.visualize_plotly(n_topics, topics)
        model.visualize_mpl(n_topics, topics)

        topic_sentiment = sentiment_analysis.sentiment_class(path)
        topic_sentiment.process_sentiment()
        topic_sentiment.save_dataframe()
        topic_sentiment.visualize(topics)

    except ValueError as e:
       print("error, maybe in topic modeling:", e)

    except KeyboardInterrupt:
       print("Ctrl-C!")
       raise

    except BaseException:
       print("uhoh base exception. What's wrong now?")
       raise


if __name__ == "__main__":
    run_pipeline()
