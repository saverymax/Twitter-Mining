import argparse
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

"""
Topic modeling on time series data
Call from commandline: python sentiment_analysis.py --file file.tsv
"""


def get_parser():
    """
    Set up command line options. In this script, the filename of the jsonl to be read must be given. Include file extension. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Modeling topics from twitter stream data") 
    parser.add_argument("--path", 
                        dest = "filename", 
                        help = "The path to the file to be analyzed. Something like /home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/tweets_converted.tsv")
    return parser


def process_tweets(data):
    """
    Vectorize and transform tweet data
    https://medium.com/mlreview/topic-modeling-with-scikit-learn-e80d33668730
    http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
    """
    
    n_features = 1000 
    n_topics = 10
    n_top_words = 10
    tfidf_vectorizer = TfidfVectorizer(max_df = 0.95, min_df = 2, max_features=n_features, stop_words='english')
    # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    # term frequency * inverse document frequency
    tfidf = tfidf_vectorizer.fit_transform(data)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    #nmf = NMF(n_components = n_topics, random_state = 1, alpha =.1, l1_ratio = .5, init= "nndsvd").fit_transform(tfidf)
    nmf = NMF(n_components=n_topics, random_state=0,alpha=.1, l1_ratio=.5).fit(tfidf)
    nmf_transform = nmf.transform(tfidf)
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    # tf_vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = n_features, stop_words='english')
    # tf = tf_vectorizer.fit_transform(data)
    # tf_feature_names = tf_vectorizer.get_feature_names()
    # print(tf_feature_names)
    # nda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    
    display_topics(nmf, tfidf_feature_names, n_top_words)
    tsne = TSNE(n_components = 2, verbose = 1, random_state = 0, angle = .99, init = 'pca').fit_transform(nmf_transform)
    visualize(tsne)

def display_topics(model, feature_names, n_top_words):
    """
    Display the most frequent words per topic
    """
    for topic_n, topic in enumerate(model.components_):
        print("Topic {}:".format(topic_n))
        print(",".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]),"\n")

def visualize(data, title = None, labels = None):
    """
    Visualize dimensionally reduced data
    """
    # take tsne plot from lecture
    if labels is None:
        c = "black"
    else:
        color_scale = np.linspace(0, 1, len(set(labels)))
        c = [plt.cm.set2(color_scale[i] for i in labels)]
    fig, ax  = plt.subplots()
    ax.scatter(data[:, 0], data[:, 1], color = c, alpha=0.75)
    plt.show()

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
    
    tweet_dataframe = pd.read_csv(args.filename, sep = '\t')

    process_tweets(tweet_dataframe['filtered_text']) 
 
