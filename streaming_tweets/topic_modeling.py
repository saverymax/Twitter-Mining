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
This script perfoms LDA of NMF on a tsv of tweet data. The tweets are clustered by topic and visualized with tSNE. References and tutorials used to write
the script can be found at the bottom. 
Here is a sample call from command line:
python topic_modeling.py --path ~/Documents/Git/Twitter-Mining/streaming_tweets/data/streaming_guns_rights_guncontrol_converted_tweets.tsv
"""


def get_parser():
    """
    Set up command line options. The filename of the jsonl to be read must be given. Include file extension in the path given in the command line. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Modeling topics from twitter stream data") 
    parser.add_argument("--path", 
                        dest = "filename", 
                        help = "The path to the file to be analyzed. Something like /home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/tweets_converted.tsv")
    return parser


class topic_modeling():
    """
    Class that contains topic modeling and visualization methods.
    """

    def __init__(self, filtered_text, original_text, dataframe):
        """
        Initiate an instance.
        Must pass the whole dataframe, and individual columns to initiate. This is unnecessary, but to generate a legend, 
        the whole dataframe is required, and I only added the legend after the rest of the script had been written.
        """

        self.dataframe = dataframe
        self.data = filtered_text
        self.tweet = original_text

    def nmf_analysis(self, n_topics):
        """
        Vectorize and transform tweet data using the NMF algorithm, which takes a tfidf matrix as input. 
        Basic tutorial below:
        http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
        """
        
        n_features = 1000 

        tfidf_vectorizer = TfidfVectorizer(max_df = 0.95, min_df = 2, max_features=n_features, stop_words='english')
        # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        # term frequency * inverse document frequency
        tfidf = tfidf_vectorizer.fit_transform(self.data)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        nmf = NMF(n_components = n_topics, random_state = 0, alpha= .1, l1_ratio = .5).fit(tfidf)
        nmf_transform = nmf.transform(tfidf)
        topic_modeling.display_topics(nmf, tfidf_feature_names)
        nmf_keys = []

        for i in range(nmf_transform.shape[0]):
            nmf_keys.append(nmf_transform[i].argmax())

        return nmf_transform, nmf_keys

    def lda_analysis(self, n_topics):
        """ 
        Vectorize and transform tweet data using LDA. LDA can only use raw term counts for LDA because it is a probabilistic graphical model,
        and hence CountVectorizer is used. 
        """

        print("Beginning LDA")
        n_features = 1000 

	# change TfidfVectorize for LDA
        tf_vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = n_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(self.data)
        tf_feature_names = tf_vectorizer.get_feature_names()
       
        lda = LatentDirichletAllocation(n_components = n_topics, learning_method = 'online', random_state = 0).fit(tf)
        lda_transform = lda.transform(tf) 
        lda_keys = []
        for i in range(lda_transform.shape[0]):
            lda_keys.append(lda_transform[i].argmax())

        self.dataframe['labels'] = pd.Series(lda_keys)

        topic_modeling.display_topics(lda, tf_feature_names)

        return lda_transform, lda_keys


    def display_topics(model, feature_names):
        """
        Display the most frequent words per topic
        """

        n_top_words = 5

        for topic_n, topic in enumerate(model.components_):
            print("Topic {}:".format(topic_n))
            print(",".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]),"\n")

    
    def run_tsne(self, transform):
        """
        Run tsne
        """

        tsne = TSNE(n_components = 2, verbose = 1, random_state = 0, angle = .99, init = 'pca').fit_transform(transform)
        return tsne


    def visualize(self, tsne_data, keys, filename, n_topics): 
        """
        Visualize dimensionally reduced data. A matplotlib plot is produced, as well as a interactive plotly plot with, after quite a hassle, a legend. 
        """

        print("Plotting...")

        #py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)

        # take tsne plot from lecture
        color_scale = np.linspace(0, 1, len(set(keys)))
        c = [plt.cm.Set2(color_scale[i]) for i in keys]
        
        # Custom colors:
        #colormap = np.array(["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
        #                     "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5"])
        
        fig, ax = plt.subplots()
        ax.set_title('{} Topics'.format(n_topics)) 
        
        # Plot with custom colors
        #ax.scatter(tsne_data[:, 0], tsne_data[:, 1], 
        #           color = colormap[keys][:len(keys)], alpha=0.75)

        # otherwise:
        ax.scatter(tsne_data[:, 0], tsne_data[:, 1], color = c, alpha=0.75)
        #plt.show()
        fig.savefig('{}.png'.format(filename))

        # working plotly stuff	 
        tsne_plot = go.Scatter(
            x = tsne_data[:, 0],
            y = tsne_data[:, 1],
            mode = "markers",
            name = "Tweet topics",
            marker = dict(color = keys, colorscale = c),
            text = self.tweet
            )
        layout = go.Layout(
           title = 'Topic modeling of tweets', 
           hovermode = 'closest'
            )
       
        data = [tsne_plot]
        # https://github.com/minimaxir/pokemon-3d/blob/master/pokemon_3d_plotly.ipynb
        #layout = go.Layout(showlegend = True)
        fig = go.Figure(data = data, layout = layout)
        plot_url = py.plot(fig)
        """
        df_palette = pd.DataFrame([
            ['0', '#A8A878'],
            ['1', '#F08030']])
           # ['fighting','#C03028'],
           # ['water','#6890F0'],
           # ['flying','#A890F0'],
           # ['grass','#78C850'],
           # ['poison', '#A040A0'],
           # ['electric', '#F8D030'],
           # ['ground', '#E0C068'],
           # ['psychic', '#F85888'],
           # ['rock', '#B8A038'],
           # ['ice', '#98D8D8'],
           # ['bug', '#A8B820'],
           # ['dragon', '#7038F8'],
           # ['ghost', '#705898']])
        
        print(self.dataframe['labels'])
        df_palette.columns = ['labels', 'typecolor']
        self.dataframe = self.dataframe.merge(df_palette, on = 'labels')

        print(self.dataframe['labels'])
        print(self.dataframe['typecolor'])
        #['dark', '#705848'],
            #['steel', '#B8B8D0'],
            #['fairy', '#EE99AC']

        # experimental plotly stuff
        self.dataframe['x'] = tsne_data[:,0]

        self.dataframe['y'] = tsne_data[:,1]
        plot_list = []

        for idx, (label, color) in df_palette.iterrows():
    #print pokemon_type
            #print(self.dataframe['keys'])

            df_filter = self.dataframe[self.dataframe['labels'].str.contains(label)]
	    
            scatter = dict(
                mode = "markers",
                name = pokemon_type.title(),
                type = "scatter3d",
                text =  df_filter['text'],
		#color=df_plot['typecolor'],
                showlegend = True,
		#legendgroup = pokemon_type.title(),
                x =  df_filter['x'], y =  df_filter['y'],
                marker = dict( size=10, color=color, 
			     line = dict(
				width = 3)))
	
            plot_list.append(scatter) 
        layout = dict(
                scene = dict(
                        xaxis = empty_axis,
                        yaxis = empty_axis,
                        ),
                showlegend = True)

        fig = dict(data=plot_list, layout=layout)
        plot_url = py.plot(fig)
        """ 

if __name__ == '__main__':
    # initiate parser 
    parser = get_parser()
    args = parser.parse_args()
    
    tweet_dataframe = pd.read_csv(args.filename, sep = '\t')
    tweet_dataframe = tweet_dataframe.dropna() 
    # Perform analysis with NMF or LDA. Would be nice to choose from command line.
    #nmf_analysis(tweet_dataframe['filtered_text']) 
    model = topic_modeling(tweet_dataframe['filtered_text'], tweet_dataframe['text'], tweet_dataframe)
    # transformed_data_nmf, keys_nmf = model.nmf_analysis()
    n_topics = 12
    transformed_data_lda, keys_lda = model.lda_analysis(n_topics)
    #tsne_nmf = model.run_tsne(transformed_data_nmf) 
    tsne_lda = model.run_tsne(transformed_data_lda) 
    #model.visualize(tsne_nmf, keys_nmf)
    model.visualize(tsne_lda, keys_lda, args.filename, n_topics)
