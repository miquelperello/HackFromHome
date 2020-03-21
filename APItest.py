# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:49 2020

@author: mike
"""
from tweepy import OAuthHandler, Stream, StreamListener, API
from PIL import Image 
from googletrans import Translator

import requests, json

paises = []
##REAL-TIME

response = requests.get("https://coronavirus-19-api.herokuapp.com/countries/") 
x = response.json()
i = 0
for todo in x:
	paises.append((todo["country"]).lower())

for all in paises:
	print (all)	

