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

api_base_url = "https://coronavirus-19-api.herokuapp.com/all"

print(response.status_code)
