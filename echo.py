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
import platform
from dotenv import load_dotenv

# external libraries:
# sr
# pyttsx3
# wikipediaAI
# requests
# psutil

load_dotenv()
weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")


battery = psutil.sensors_battery()
plugged = battery.power_plugged
percent = battery.percent

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    print(voice.id)

engine.setProperty('voice', voices[1].id)

# Speak text function
def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def introduce():
    speak("Hello, I am Echo, your AI voice assistant.")

# Function to greet user
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")
    speak("How can I help you?")

# Function to listen to microphone input
def listen():
    r = sr.Recognizer()
    query = ""
    microphone = sr.Microphone()
    with microphone as source:
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

def listInternet():
    # Run the 'netsh wlan show networks' command to scan for Wi-Fi networks
    output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], universal_newlines=True)

    # Split the output into lines and print the names of the networks
    for line in output.splitlines():
        if 'SSID' in line:
            network_name = line.split(': ')[1]
            speak(network_name)

# Function to search Wikipedia
def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    speak(results)

# Function to get weather information
def get_weather():
    api_key = weather_api_key
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

def open_app(app_location):
    subprocess.Popen(app_location)      

def get_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    data = json.loads(response.text)
    print('Your location:' + ' ' + data['city'] + ' '  + data['country'])
    speak('Your location:' + ' ' + data['city'] + ' '  + data['country'])

def search(query):
    query = query.replace("search", "")
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)

def calc(query):
    # remove "what is" from the input text
    calculation_query = query.replace("what is", "")
    # evaluate the math expression
    calculation_query.replace("x", "*")
    calculation_query.replace("times", "*")
    calculation_query.replace("by", "*")
    try:
        result = eval(calculation_query)
        speak("The result is " + str(result))
    except:
        speak("Sorry, I couldn't calculate that.")

# Main function to run the virtual assistant
if __name__ == "__main__":
    greet()
    while True:
        query = listen()
        if query:
            if 'search' in query.lower():
                search(query)
            elif 'wikipedia' in query.lower():
                search_wikipedia(query)
            elif 'battery' in query.lower():
                if plugged:
                    speak(f"The battery is {percent}%, and the power cable is plugged in.")
                else:
                    speak(f"The battery is {percent}%, and the power cable is not plugged in.")
            elif 'echo' in query.lower():
                greet()
                speak("Hello Sir, How may I assist you today")
            elif 'hello' in query.lower() or 'hi' in query.lower():
                greet()
            elif 'shutdown' in query.lower() or 'bye' in query.lower() or 'shut down' in query.lower():
                speak("Goodbye!")
                break
            elif 'weather' in query.lower():
                get_weather()
            elif "youtube" in query.lower():
                webbrowser.open("https://www.youtube.com")
            elif "gmail" in query.lower():
                webbrowser.open("https://www.gmail.com")
            elif "google" in query.lower():
                webbrowser.open("https://www.google.com")
            elif "what time is it" in query.lower():
                time = datetime.datetime.now().strftime("%H:%M")    
                speak(f"The time is {time}")
            elif "internet" in query.lower():
                returnInternet()
            elif "list wifi" in query.lower() or "list wi-fi" in query.lower():
                listInternet()
            elif "location" in query.lower():
                get_location()
            elif "what is" in query.lower():
                calc(query)
            else:
                speak("Sorry, I am not programmed to respond to that command.")
        else:
            speak("Sorry I didn't catch that")
