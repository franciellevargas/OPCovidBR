# -*- coding: utf-8 -*- 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tweepy
import re

# acessar a aba "Keys and Access Tokens"
# passa o Consumer Key e o Consumer Secret
auth = tweepy.OAuthHandler('46pvnSwIVylfWepbPsP4433wL', 'xWDPHaUkk0ub93qj1DaYgJcO8QtkPUhNFIE7uBAvzbSVLLpLzR')

# define o token de acesso
# para criar basta clicar em "Create my access token"
# passa o "Access Token" e o "Access Token Secret"
auth.set_access_token('1952916806-9WbU9ROPLd4aVPprQZqWJhaW4RSXrBw4oK8A4Ow',
		'gW5iuYPtrTxVhPmQxBemsKz6jCAOqbYx1fT0ewKHFyAkG')

# cria um objeto api
api = tweepy.API(auth)
search_term = 'coronavírus'
search_term2 = 'codiv-19'

c=tweepy.Cursor(api.search,
            q="{}+OR+{}".format(search_term,search_term2),
            rpp=1000,
            lang='pt',
            include_entities=True)

data = {}
i = 1
for tweet in c.items():
    data['text'] = tweet.text
    print(i, ":", data)
    i += 1
time.sleep(1)
