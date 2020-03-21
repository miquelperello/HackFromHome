# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:49 2020

@author: mike
"""
from tweepy import OAuthHandler, Stream, StreamListener, API
from PIL import Image 
from googletrans import Translator

import requests, json


##REAL-TIME

response = requests.get("https://coronavirus-19-api.herokuapp.com/countries/spain") 

print(response.json())

print(response.json()['deaths'])

