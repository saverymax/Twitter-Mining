# What's going on with Trump and Twitter?

President Trump's most commonly used words, in his 500 most recent tweets
![Trumps most commonly used words in his 500 most recent tweets](/figures/trump_data/trump_terms.png)

And his most common hashtags
![Trumps most commonly used hashtags in his 500 most recent tweets](/figures/trump_data/trump_hashtags.png)

To get an idea of what trump topics about, here is the t-SNE plot of an LDA topic model. Each point is a tweet. Hover your mouse over each one to the text of the tweet. The legend shows the words that most represent each topic cluster. 

However, since this is a relatively small data set, the LDA algorithm does not do a super great job of clustering tweets, and there are definitely some tweets that do not really belong in the cluster they have been grouped in. I'll include another plot that does not include any tweets with a low probability of being in any given cluser. 
[See the plot here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_model_trump)


See an interactive time series documenting Trump's tweets and tweet metrics, from December 2017 to March 2018 
[here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/trump_time_series)

And a time series from March 2017 through May
[here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/trump_series_early2018)

