# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:49 2020

@author: mike
"""
from tweepy import OAuthHandler, Stream, StreamListener, API
from PIL import Image 
from googletrans import Translator

import requests, json

from bs4 import BeautifulSoup
from PIL import Image 
import requests



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="K6L8pQamwrVrIT1Qacvjtx9yW"
consumer_secret="ndjXdABlQxlGeyAT7WcBdNcTq7sQzZkTYusJSkWhBBw9hmhYEX"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1241308792526123009-crprGTXVZuWM2Z3NHwecJQdEnL6dXD"
access_token_secret="5XYEQz9DzbpRIb9TBg7PHxbK7B9q52yZx4FoBRYBTgz9L"


	
##REAL-TIME
paises = []



def guardapaisosdisponibles():	
		response = requests.get("https://coronavirus-19-api.herokuapp.com/countries/") 
		x = response.json()
		i = 0
		for todo in x:
			paises.append((todo["country"]).lower())


	


class StdOutListener(StreamListener):
  
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
       	prediction(statID, author, text)
       return True

    def on_error(self, status):
        print(status)




def checkifpaisexiste(pais):
	if pais.lower() not in paises:
		return False
	else:
		return True


def busquedainfoprediction():  
	url = 'https://biocomsc.upc.edu/en/covid-19'
	# get contents from url
	content = requests.get(url).content

	soup = BeautifulSoup(content,'lxml')
	
	dades = []

	for table in soup.find_all("table",{"class":"plain"}):
		for finded in table.find_all("td"):
			for ili in finded.find_all("p"):
				dades.append(ili.getText())

	predCatDema = dades[2]
	predCatPassat = dades[4]
	predCatAltre = dades[6]


	predEspDema = dades[9]
	predEspPassat = dades[11]
	predEspAltre = dades[13]


	predUEDema = dades[17]
	predUEPassat = dades[19]
	predUEAltre = dades[21]


	#images
	image_tags = soup.findAll('img')
	i = 0
	for image_tag in image_tags:
		url = image_tag.get('src')
		image_file = Image.open(requests.get(url, stream=True).raw)
		name =  str(i) + ".png"
		image_file.save(name) 
		i = i+1

def prediction(tweetid, author, text):
	text = text.lower()

	if ("catalunya" in text or "catalonia" in text or "cataluña" in text):
		avui = predCatDema 
		dema = predCatPassat 
		altre = predCatAltre 
	elif  ("españa" in text or "espanya" in text or "spain" in text):
		avui = predEspDema 
		dema = predEspPassat 
		altre = predEspAltre 

	elif ("ue" in text or "europea" in text or "europa" in text or "europe"):
		avui = dades[17]
		dema = dades[19]
		altre = dades[21]

	filename = "1.png"
	x = datetime.datetime.now()
	api.update_with_media(filename, status = "Hey, @" +author +". The predictions for the next three days, according to the information gived by BIOCOM-SC, are:  "+ avui + ", " + dema + ", " + altre  , in_reply_to_status_id = tweetid)









def respondrealtime(tweetid, author, text):
	pais = text
	print (pais)
	if (checkifpaisexiste(pais) == True):
		web_api = "https://coronavirus-19-api.herokuapp.com/countries/" + pais
		response = requests.get(web_api)
		x = response.json() 
		if response.json()['cod'] != "404": 
			print(response.json())
			actualdeaths = response.json()['deaths']
			cases = response.json()['cases']
			todaycases = response.json()['todayCases']
			recovered = response.json()['recovered']
			active = response.json()['active']
			
			api.update_status("Hi, @" +author + ".\n👑🦠 cases: " + str(cases) +  "\n 💀 deaths: " + str(actualdeaths) + "\n 🏥 active:  " + str(active) + "\n💪 recovered : " + str(recovered) , in_reply_to_status_id = tweetid) 
			    
	else: 
		    api.update_status("Ups! @"+ author +". Sorry! The country does not exist!😯", in_reply_to_status_id = tweetid) 
	
	return True

guardapaisosdisponibles()
busquedainfoprediction()

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

stream = Stream(auth, l)
stream.filter(track=['@cobot_19'])

