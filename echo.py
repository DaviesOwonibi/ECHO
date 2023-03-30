import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import requests
import json
import webbrowser
import os
import subprocess
import psutil
import urllib.request
import wolframalpha
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Authenticate with the Wolfram API using a stored API key
client = wolframalpha.Client("GWAE2J-WHE878TEUT")

def tellFact():
	# Query the Wolfram API for a generic fact
	res = client.query("Tell me a fact")

	# Extract and print the result
	try:
		print(next(res.results).text)
	except:
		print("I cant get a fact right now.")

def calc(query):
	# remove "what is" from the input text
	cquery = query.replace("what is", "")

	# evaluate the math expression
	try:
		result = eval(cquery)
		engine.say("The result is " + str(result))
		engine.runAndWait()
	except:
		engine.say("Sorry, I couldn't calculate that.")
		engine.runAndWait()

def checkInternet():
	try:
		urllib.request.urlopen('http://www.google.com')
		return True
	except:
		return False

def returnInternet():
	if checkInternet() == True:
		speak("You are connected")
	else:
		speak("You are disconnected")

battery = psutil.sensors_battery()
plugged = battery.power_plugged
percent = battery.percent

chrome_path = "/Applications/Google Chrome.app"
webbrowser.BackgroundBrowser(chrome_path)
# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[7].id)

def openChromeApp(app):
	app = app.replace("open chrome app", "")
	chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
	app_url = "chrome://apps/" + app
	subprocess.call([chrome_path, "--app=" + app_url])

# Speak text function
def speak(text):
	engine.say(text)
	engine.runAndWait()

def increaseVolume(value):
	value = value.replace("increase", "")
	value = int(value)
	# build the AppleScript command to increase the volume
	applescript = f"set volume output volume ((output volume of (get volume settings)) + {value})"

	# execute the AppleScript command using osascript
	os.system(f"osascript -e '{applescript}'")
	speak("Volume was increased by" + str(value) + "%")

def decreaseVolume(value):
	value = value.replace("decrease", "")
	value = int(value)
	# build the AppleScript command to increase the volume
	applescript = f"set volume output volume ((output volume of (get volume settings)) - {value}{{}}"

	# execute the AppleScript command using osascript
	os.system(f"osascript -e '{applescript}'")
	speak("Volume was decreased by" + str(value) + "%")

# Function to greet user
def greet():
	hour = int(datetime.datetime.now().hour)
	if hour >= 0 and hour < 12:
		speak("Good morning, my name is Echo! How can I help you?")
	elif hour >= 12 and hour < 18:
		speak("Good afternoon, my name is Echo! How can I help you?")
	else:
		speak("Good evening, my name is Echo! How can I help you?")


# Function to listen to microphone input
def listen():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)


	try:
		print("Recognizing...")
		query = r.recognize_google(audio, language='en-in')
		print(f"You said: {query}\n")
	except Exception as e:
		print("Sorry, I didn't catch that. Can you please repeat?")
		query = None


	return query


# Function to search Wikipedia
def search_wikipedia(query):
	speak("Searching Wikipedia...")
	query = query.replace("wikipedia", "")
	results = wikipedia.summary(query, sentences=2)
	speak("According to Wikipedia")
	speak(results)


# Function to get weather information
def get_weather():
	api_key = 'ad2996b6abc8596852c26bb139cffbe3'  # replace with your own OpenWeatherMap API key
	base_url = "http://api.openweathermap.org/data/2.5/weather?"


	# get user location
	ip_request = requests.get('https://get.geojs.io/v1/ip.json')
	ip_address = ip_request.json()['ip']
	url = 'https://get.geojs.io/v1/ip/geo/' + ip_address + '.json'
	location_request = requests.get(url)
	location_data = location_request.json()


	# get weather data for user location
	city = location_data['city']
	country = location_data['country']
	complete_url = base_url + "appid=" + api_key + "&q=" + city + "," + country
	response = requests.get(complete_url)
	weather_data = response.json()


	# parse weather data and speak the current weather conditions
	if weather_data['cod'] != '404':
		temperature = round(weather_data['main']['temp'] - 273.15)  # convert from Kelvin to Celsius
		description = weather_data['weather'][0]['description']
		speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
	else:
		speak("Sorry, I couldn't get the weather information for your location.")


def get_location():
	url = 'https://ipinfo.io/json'
	response = requests.get(url)
	data = json.loads(response.text)
	speak('Your location:' + ' ' + data['city'] + ' '  + data['country'])

def search(query):
	query = query.replace("search", "")
	url = "https://www.google.com/search?q=" + query
	webbrowser.open(url)


# Main function to run the virtual assistant
if __name__ == "__main__":
	greet()
	while True:
		query = listen()
		if query is not None:
			if 'wikipedia' in query.lower():
				search_wikipedia(query)
			elif 'tell me a fact' in query.lower():
				tellFact()
			elif 'search' in query.lower():
				funQuery = query.replace("search", "")
				search(query)
				speak(funQuery + "was searched.")
			elif "increase" in query.lower():
				increaseVolume(query)
			elif "decrease" in query.lower():
				decreaseVolume(query)
			elif 'battery' in query.lower():
				if plugged:
					speak(f"The battery is {percent}%, and the power cable is plugged in.")
				else:
					speak(f"The battery is {percent}%, and the power cable is not plugged in.")
			elif 'echo' in query.lower():
				speak("Hi, How may I assist you to day")
			elif 'hello' in query.lower() or 'hi' in query.lower():
				greet()
			elif 'weather' in query.lower():
				get_weather()
			elif "youtube" in query.lower():
				webbrowser.open("https://www.youtube.com")
				speak("Youtube Opened.")
			elif "gmail" in query.lower():
				webbrowser.open("https://www.gmail.com")
				speak("Gmail Opened.")
			elif "google" in query.lower():
				webbrowser.open("https://www.google.com")
				speak("Google Opened.")
			elif "chat" in query.lower():
				webbrowser.open("https://chat.openai.com/chat")
				speak("Chat,G,P,T Opened.")
			elif "time" in query.lower():
				time = datetime.datetime.now().strftime("%H:%M")
				speak(f"The time is {time}")
			elif "location" in query.lower():
				get_location()
			elif "internet" in query.lower():
				returnInternet()
			elif "what is" in query.lower():
				calc(query)
			elif 'shutdown' in query.lower() or 'bye' in query.lower() or 'shut down' in query.lower():
				speak("Shutting Down, Goodbye!")
				break
			else:
				speak("Sorry, I am not programmed to respond to that command.")
