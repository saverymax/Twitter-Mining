import argparse
import plotly_credentials
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation 

"""
Topic modeling on time series data
Sample call from commandline:
python topic_modeling.py --path ~/Documents/Git/Twitter-Mining/streaming_tweets/data/streaming_guns_rights_guncontrol_converted_tweets.tsv
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


def nmf_analysis(data):
    """
    Vectorize and transform tweet data
    Basic tutorial below:
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

    nmf = NMF(n_components=n_topics, random_state=0,alpha=.1, l1_ratio=.5).fit(tfidf)
    nmf_transform = nmf.transform(tfidf)
    display_topics(nmf, tfidf_feature_names, n_top_words)
    run_tsne(nmf_transform)

def lda_analysis(data):
    """ 
    LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    """

    n_features = 1000 
    n_topics = 10

    tf_vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = n_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(data)
    tf_feature_names = tf_vectorizer.get_feature_names()
    #print(tf_feature_names)
   
    lda = LatentDirichletAllocation(n_components = n_topics, max_iter = 5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    lda_transform = lda.transform(tf) 
    lda_keys = []
    for i in range(lda_transform.shape[0]):
        lda_keys.append(lda_transform[i].argmax())

    #display_topics(lda, tf_feature_names, n_top_words)
    run_tsne(lda_transform, lda_keys, data)
 
def run_tsne(transform, keys, data):
    """
    Run tsne
    """

    tsne = TSNE(n_components = 2, verbose = 1, random_state = 0, angle = .99, init = 'pca').fit_transform(transform)
    visualize(tsne, keys, data)


def display_topics(model, feature_names):
    """
    Display the most frequent words per topic
    """

    n_top_words = 10

    for topic_n, topic in enumerate(model.components_):
        print("Topic {}:".format(topic_n))
        print(",".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]),"\n")


def visualize(tsne_data, keys, data): 
    """
    Visualize dimensionally reduced data
    """

    py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)

    # take tsne plot from lecture
    color_scale = np.linspace(0, 1, len(set(keys)))
    c = [plt.cm.Set2(color_scale[i]) for i in keys]
    
    # Custom colors:
    #colormap = np.array(["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
    #                     "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5"])
    
    fig, ax = plt.subplots()
    
    # Plot with custom colors
    #ax.scatter(tsne_data[:, 0], tsne_data[:, 1], 
    #           color = colormap[keys][:len(keys)], alpha=0.75)

    # otherwise:
    ax.scatter(tsne_data[:, 0], tsne_data[:, 1], color = c, alpha=0.75)
    plt.show()

    tsne_plot = go.Scatter(
            x = tsne_data[:, 0],
            y = tsne_data[:, 1],
            mode = "markers",
            name = "Tweet topics",
            marker = dict(color = keys, colorscale = c),
            text = data
            )
    datas = [tsne_plot] 
    plot_url = py.plot(datas) 

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
    
    tweet_dataframe = pd.read_csv(args.filename, sep = '\t')

    #nmf_analysis(tweet_dataframe['filtered_text']) 
    
    lda_analysis(tweet_dataframe['filtered_text']) 
     
