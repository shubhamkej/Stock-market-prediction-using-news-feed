from django.shortcuts import render
from django.http import HttpResponse
import random
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
from trailapp import keys
import numpy as np
import pandas as pd
from nsetools import Nse

from datetime import datetime
from nsepy import get_history
import dateutil.relativedelta
from IPython.display import HTML, display

def index(request):    
    return render(request,'trailapp/index.html')

def historical(request):
    if request.method == "GET":
        nse = Nse()
        if request.GET['stockname']:
            company_name = request.GET['stockname']
            q = nse.get_quote(company_name)
            to_date = datetime.now()
            to_date = datetime.strftime(to_date, '%Y,%m,%d')
            to_date = datetime.strptime(to_date, '%Y,%m,%d')
            from_date = to_date - dateutil.relativedelta.relativedelta(days=7)
            ans = get_history(symbol=company_name, start=from_date, end=to_date)

    company = { 
        'company_name' : q['companyName'],
        'df' : ans,
    }
    print(company['df'])
    context = {
        'company_details' : company,
    }
    print("done")
    return render(request, 'trailapp/historical.html', context)

#STOCK DETAILS
def stocks(request):
    print("stock")
    nse = Nse()
    if request.method == "GET":
        company_name = request.GET['stockname']
        q = nse.get_quote(company_name) # it's ok to use both upper or lower case for codes.
    print(q['companyName'])
    print(q)    
    company = { 
        'company_name' : q['companyName'],
        'company_symbol' : q['symbol'],
        'isin_code' : q['isinCode'],
        'company_series' : q['series'],
        'company_status' : q['css_status_desc'],
        'company_close' : q['closePrice'],
        'company_open' : q['open'],
        'company_high' : q['dayHigh'],
        'company_low' : q['dayLow'],
        'current_price' : q['lastPrice'],
        'previous_close' : q['previousClose']
    }
    context = {
        'company_details' : company
    }
    return render(request,'trailapp/stocks.html',context)

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
        auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

#Just get random company    
def getRandomCompany():
    keep = ['@amazonIN', '@YESBANK', '@HDFC_Bank','@JetBlue','@innocent']
    randomNumber = random.randint(0,4)
    return keep[randomNumber]
def tweets(request):
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    myCount = datetime.datetime.now()

    twitterHandle1 = getRandomCompany()
    tweets1 = api.user_timeline(screen_name=twitterHandle1,count= 2)

    twitterHandle2 = getRandomCompany()
    tweets2 = api.user_timeline(screen_name=twitterHandle2,count= 2)
    
    twitterHandle3 = getRandomCompany()
    tweets3 = api.user_timeline(screen_name=twitterHandle3,count= 2)

    df = tweet_analyzer.tweets_to_data_frame(tweets1)
    df1 = tweet_analyzer.tweets_to_data_frame(tweets2)
    df2 = tweet_analyzer.tweets_to_data_frame(tweets3)

    data = {'company_name' : twitterHandle1,'tweet' : df['Tweets'][0],
    'date' : df['date'][0], 'likes': df['likes'][0]}
    
    data1 = {'company_name' : twitterHandle2,'tweet' : df1['Tweets'][0],
    'date' : df1['date'][0], 'likes': df1['likes'][0]}
    
    data2 = {'company_name' : twitterHandle3,'tweet' : df2['Tweets'][0],
    'date' : df2['date'][0], 'likes': df2['likes'][0]}
    context = {
        'data' : data, 'data1' : data1, 'data2' : data2
    }
    print(df['Tweets'][0])
    return render(request,"trailapp/tweets.html",context)