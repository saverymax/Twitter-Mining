import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

def visualize():
    # https://plot.ly/matplotlib/bar-charts/ as reference
    # Sign in to plotly
    py.sign_in('savery_max', 'GZgmuV5Y6ERRSdx2wG8B')
    labels = ['a', 'b', 'c']
    indexes = np.arange(len(labels))
    width = 1 
    freq = (5,2,2)
    tweet_figure, axis = plt.subplots() 
    axis.bar(indexes, freq, width,tick_label= (('a','b','c')),color = 'red')

    axis.set_xticks(indexes + width) # Changing width sets the x tick 
    
    axis.set_xticklabels(('a','b','c'))# , rotation = 55)
    axis.set_xlabel('Terms used')
    axis.set_ylabel('Frequency of terms')
    axis.set_title('Term usage of Twitter Users')
    plt.show() 
    # Online plotting isn't adding xtick labels. Don't care to find out why.  
    plotly_fig = tls.mpl_to_plotly(tweet_figure)
    url = py.plot_mpl(tweet_figure, filename = "tweet_frequency")   

visualize()
