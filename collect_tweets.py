#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:10:36 2019

@author: aleidaolvera
"""

import tweepy as tw
import pandas as pd

consumer_key = 'nPmaGDKWK53vMj6Q2MGPk1Ubl'
consumer_secret = 'gWyYgClxTpvynetZyk5ZfI4oUD6M0sUVxCBaTI6owQm0mUefzT'

access_token = '2569634298-ZDGIczXFvWhNpuBdhv08tcCnozeQW7i0uta7Yyw'
access_token_secret = 'HWfydzmrYEQLK0mAfIQOO7UI0bJjaezLUKGkCVwSr6aGr'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#gentrification"
date_since = "2016-01-01"

new_search = search_words + " -filter:retweets"

tweets = tw.Cursor(api.search, 
                           q=new_search,
                           lang="en",
                           since=date_since).items(3000)

all_tweets = [[tweet.user.screen_name, tweet.text] for tweet in tweets]

tweets_gentrification = [[tweet.user.screen_name, tweet.user.location, tweet.text] for tweet in tweets]


