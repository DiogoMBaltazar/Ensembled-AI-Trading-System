import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import time
import flair
import tweetstream
import pandas as pd
import GetOldTweets3 as got
from Utilities.config import *
from Utilities.util_funcs import *
from Utilities.Database_funcs import *

sentiment_model = flair.models.TextClassifier.load('en-sentiment')

##############################################################################
# Class that holds functions that can get past x tweets from a list of users,
# get live tweets also from a list and  search for a given ticker mentions
##############################################################################



# https://towardsdatascience.com/sentiment-analysis-for-stock-price-prediction-in-python-bed40c65d178
# https://huggingface.co/transformers/model_doc/roberta.html
# https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1

begin_time = datetime.datetime.now()


class Twitter_Sentiment(object):
    
    def __init__(self):
        
        print("|---------------------------------------------|")
        print("|Twitter Sentiment Engine has been initialized|")
        print("|---------------------------------------------|")

        pass



    def live_tweets_list_users(self, twitter_users_list):

        self.users_list = twitter_users_list

        print("|-----------------------------------------------------------------|")
        print(f"Checking live tweets for", len(self.users_list), "users mentioned in the config list")
        print("|-----------------------------------------------------------------|")

        date_list = []
        user_list = []
        tweet_list = []
        likes_list = []
        retweets_list = []
        tickers_list = []

        for user in self.users_list:
            
            try:     
                
                # Creation of query method using parameters
                tweets = twitter_api.user_timeline(screen_name=user,count=3, include_rts = True,tweet_mode = 'extended')

                status = tweets[0]

                date_list.append(status.created_at)
                user_list.append(status.user.name)
                tweet_list.append(status.full_text)
                likes_list.append(status.favorite_count)
                retweets_list.append(status.retweet_count)

                # Grabbing tickers from tweet
                ticker = re.findall(r'[$][A-Za-z][\S]*', status.full_text)
                tickers_list.append(ticker)

            except tweepy.TweepError as e:
                if e.response.status_code == 34:
                    print(f"User {user} doesn't exist.")
                elif e.response.status_code == 420:
                    print("Disconnected from stream")
                pass
            

        recent_tweets_df = pd.DataFrame({'Date': date_list, 'User': user_list,
                   'Ticker': tickers_list, 'Tweet': tweet_list, 
                   "Likes": likes_list, 'Retweets': retweets_list})

            
        # Cleaning Tweets
        recent_tweets_df["Tweet"] = recent_tweets_df["Tweet"].map(lambda x: cleaner(x))
        

        # Calculating sentiment using Blob, Vader and roBERTa (transformer)
        recent_tweets_df['Blob sentiment'] = recent_tweets_df["Tweet"].map(lambda x: blob_sentiment(x))
        recent_tweets_df['Vader sentiment'] = recent_tweets_df["Tweet"].map(lambda x: vader_sentiment(x))
        recent_tweets_df['roBERTa sentiment'] = recent_tweets_df["Tweet"].map(lambda x: roBERTa_sentiment(x))
        final_sentiment(recent_tweets_df)

        # recent_tweets_df.to_csv('') #specify location

        end_time = datetime.datetime.now() - begin_time
        print('\033[94m' + f'This script took %s', end_time, "seconds to run")


        return recent_tweets_df

    
    
    def ticker_tweets(self, symbol, since_date, until_date, count):
        
        """ Date input format should be YY-MM-DD and count depends on the asset class 
        and given liquidity"""

        self.symbol = symbol 
        self.since_date = since_date 
        self.until_date = until_date 

        self.count = count
        
        # Creation of query object
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(self.symbol).setSince(since_date).setUntil(until_date).setMaxTweets(count)


        print(tweetCriteria)
