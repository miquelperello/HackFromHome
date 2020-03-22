# -*- coding: utf-8 -*-
"""
Created on 21/3/2020

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
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""


	
##REAL-TIME
paises = []

predCatDema = "" 
predCatPassat = ""
predCatAltre = ""


predEspDema= ""
predEspPassat = ""
predEspAltre = ""


predUEDema = ""
predUEPassat = ""
predUEAltre = ""

def guardapaisosdisponibles():	
		response = requests.get("https://coronavirus-19-api.herokuapp.com/countries/") 
		x = response.json()
		i = 0
		for todo in x:
			paises.append((todo["country"]).lower())

def checkifpaisexiste(pais):
	if pais.lower() not in paises:
		return False
	else:
		return True


dades = []

def busquedainfoprediction():  
	url = 'https://biocomsc.upc.edu/en/covid-19'
	# get contents from url
	content = requests.get(url).content

	soup = BeautifulSoup(content,'lxml')
	
	

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
	tipo = ""
	if ("catalunya" in text or "catalonia" in text or "cataluña" in text):
		avui = dades[2]
		dema = dades[4]
		altre = dades[6]
		tipo = "Catalonia"
		 
	elif  ("españa" in text or "espanya" in text or "spain" in text):
		avui = dades[9]
		dema = dades[11]
		altre = dades[13]
		tipo = "Spain"

	elif ("ue" in text or "europea" in text or "europa" in text or "europe"):
		avui = dades[17]
		dema = dades[19]
		altre = dades[21]
		tipo = "Europe"

	filename = "1.png"
	api.update_with_media(filename, status = "Hey, @" +author +". The projections for the next three days in " + tipo +", according to the information given by BIOCOM-SC, are:  "+ avui + ", " + dema + " and " + altre + " cases!😰. #StayHomeStaySafe" , in_reply_to_status_id = tweetid)

def respondrealtime(tweetid, author, text):
	pais = text
	print (pais)
	if (checkifpaisexiste(pais) == True):
		web_api = "https://coronavirus-19-api.herokuapp.com/countries/" + pais
		response = requests.get(web_api)
		x = response.json() 
		print(response.json())
		actualdeaths = response.json()['deaths']
		cases = response.json()['cases']
		todaycases = response.json()['todayCases']
		recovered = response.json()['recovered']
		active = response.json()['active']
		api.update_status("Hi, @" +author + ".\n👑 cases: " + str(cases) +  "\n 💀 deaths: " + str(actualdeaths) + "\n 🏥 active:  " + str(active) + "\n💪 recovered : " + str(recovered) , in_reply_to_status_id = tweetid) 
			    
	else: 
		    api.update_status("Ups! @"+ author +". Sorry! The country does not exist!😯", in_reply_to_status_id = tweetid) 
	
	return True

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



guardapaisosdisponibles()
busquedainfoprediction()

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

stream = Stream(auth, l)
stream.filter(track=['@cobot_19'])

