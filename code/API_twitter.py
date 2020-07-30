# -*- coding: utf-8 -*-
#/usr/local/lib/python3.6

import tweepy
import re
#Autentication API Twitter number 12
auth = tweepy.OAuthHandler('46pvnSwIVylfWepbPsP4433wL', 'xWDPHaUkk0ub93qj1DaYgJcO8QtkPUhNFIE7uBAvzbSVLLpLzR')
auth.set_access_token('1952916806-9WbU9ROPLd4aVPprQZqWJhaW4RSXrBw4oK8A4Ow', 'gW5iuYPtrTxVhPmQxBemsKz6jCAOqbYx1fT0ewKHFyAkG')
api = tweepy.API(auth)


tweets = api.search(q="coronavírus", lang="pt", count=2000, tweet_mode='extended')
i = 1
data = {}
for tweet in tweets:
    try:
    	data['text'] = tweet.retweeted_status.full_text
    	print(i, data)
    	i += 1
    except AttributeError:  # Not a Retweet
    	data['text'] = tweet.full_text
    	print(i, data)
    	i += 1
