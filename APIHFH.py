# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:49 2020

@author: mike
"""
from tweepy import OAuthHandler, Stream, StreamListener, API
from PIL import Image 
from googletrans import Translator

import requests, json



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="K6L8pQamwrVrIT1Qacvjtx9yW"
consumer_secret="ndjXdABlQxlGeyAT7WcBdNcTq7sQzZkTYusJSkWhBBw9hmhYEX"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1241308792526123009-crprGTXVZuWM2Z3NHwecJQdEnL6dXD"
access_token_secret="5XYEQz9DzbpRIb9TBg7PHxbK7B9q52yZx4FoBRYBTgz9L"


##REAL-TIME






class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_status(self, status):
       print (status.author.screen_name, status.created_at, status.text, status.id)
       author = status.author.screen_name
       text = status.text
       statID = status.id
       if "info" in text:
       	end = len(text)
       	print(end)
       	text= text[15:end]
       	print(text)
       	respondrealtime(statID, author, text)
       elif "prediction" in text:	
       	"""image = status.entities["media"][0]["media_url"]
       	converteiximatge(image)
       	respondimatge(statID, author)"""
       return True

    def on_error(self, status):
        print(status)

def converteiximatge(url): 
	image_file = Image.open(requests.get(url, stream=True).raw)
	image_file = image_file.convert('1') # convert image to black and white
	image_file.save("C:\\projectes\\APITwitter\\result.png")

def respondimatge(tweetid, author):
	filename = "C:\\projectes\\APITwitter\\result.png"
	api.update_with_media(filename, status = "Hey, @" +author , in_reply_to_status_id = tweetid)

def respondrealtime(tweetid, author, text):
	pais = text
	print (pais)
	web_api = "https://coronavirus-19-api.herokuapp.com/countries/" + pais
	response = requests.get(web_api) 
	print(response.json())
	actualdeaths = response.json()['deaths']
	cases = response.json()['cases']
	todaycases = response.json()['todaycases']
	recovered = response.json()['recovered']
	active = response.json()['active']
	
	api.update_status("Hi, @" +author + ".👑🦠 cases: " + cases +  "\n 💀: " + str(actualdeaths) + "\n 🏥 active:  " + active + "💪 recovered : " + recovered , in_reply_to_status_id = tweetid) 
	    
	 

	"""
		else: 
		    api.update_status("@"+ author +" Sorry! City Not Found", in_reply_to_status_id = tweetid) 
	"""
	return True


l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

stream = Stream(auth, l)
stream.filter(track=['@cobot_19'])