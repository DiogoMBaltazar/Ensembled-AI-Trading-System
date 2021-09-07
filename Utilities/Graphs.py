import sys

from pandas.core.frame import DataFrame
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Strategies.Facebook_Prophet import FBProphet

# plt.style.available
plt.style.use("seaborn-darkgrid")

class Graphs(object):


    def pca_components(data, pca):

        # Plot to find optimal number of components
        plt.axhline(y=0.9, color='r', linestyle='-') # change y accordingly

        plt.text(0.5, 0.85, '90% cut-off threshold', color = 'red', fontsize=16)
        plt.plot(np.cumsum(pca.explained_variance_ratio_))
        plt.xlabel('number of components')
        plt.ylabel('cumulative explained variance');
        plt.xlim(0, 40)
        
        return plt.show()

    def fb_prophet_graph(self, model, predictions, symbol):

        self.model = model
        self.forecast = predictions
        self.symbol = symbol

        self.model.plot(self.forecast)

        # self.model.plot_components(self.forecast)

        plt.title(f"Prediction of {self.symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Closing Stock Price")
        
        return plt.show()


    def sentiment_analysis(self, data):

        self.data = data

        return self.data.sentiment.value_counts().plot(kind='bar', title='sentiment analysis')



    def close_price(self, data, symbol):

        self.data = data
        self.symbol = symbol


        self.data.plot(y='close', x='date', figsize=(15, 7))
        plt.title(f"{self.symbol}")

        return plt.show()


    def ftt_transformation(self, fft_list, symbol):

        plt.figure(figsize=(15, 7))
        plt.plot(np.fft.ifft(fft_list))
        
        return plt.show()



    def facebook_prophet(self, forecast, symbol):

        
        plt.rc("font", family="arial", size=16)

        fig, ax = plt.subplots();
        ax.plot(forecast["ds"], forecast["yhat"], linewidth=2, color="#F59B00", label="model")
        ax.plot(forecast["ds"], input_df["y"], label="BTC")
        plt.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="#F59B00", alpha=0.2)
        plt.xlabel("Year");
        plt.ylabel("USD$");
        plt.title(f"{symbol} Price Initial Model");
        plt.legend()

        return plt.show()


    def RL_agents(self, env):

        self.env = env
        
        plt.figure(figsize=(15,6))
        plt.cla()
        self.env.render_all()

        return plt.show()
