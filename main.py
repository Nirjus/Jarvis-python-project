import speech_recognition as sr  # Import the speech recognition library
import webbrowser  # Import the web browser library to open URLs
import pyttsx3  # Import the text-to-speech library
import os
import requests
from dotenv import load_dotenv
import musiclibrary
from GeminiAi import generateAI
# Load environment variables from .env file
load_dotenv()

recognizer = sr.Recognizer()  # Create an instance of the Recognizer class from the speech_recognition library
engine = pyttsx3.init()  # Initialize the text-to-speech engine
newsApi = os.environ['NEWS_API']

def speak(text):
    """ RATE"""
    engine.setProperty('rate',140)
    """VOICE"""
    voices = engine.getProperty('voices') 
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait for the speech to finish

def processCommand(c):
    # Open different websites based on the spoken command
    if c.lower() == "open google":
        webbrowser.open("https://google.com")
    elif c.lower() == "open facebook":
        webbrowser.open("https://facebook.com")
    elif c.lower() == "open youtube":
        webbrowser.open("https://youtube.com")
    elif c.lower() == "open linkedin":  # Corrected spelling of LinkedIn
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}")
        if r.status_code == 200:
            data = r.json()
            # extract data
            articles = data.get('articles',[])
            # speak the headlines
            for articl in articles:
                speak(articl['title'])
    else:
    # let Gmini AI handle the requiest
        output = generateAI(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")  # Speak initialization message
    while True:
        try:
            with sr.Microphone() as source:  # Use the microphone as the audio source
                print("Listening for wake word...")
                # Listen for audio input with a timeout of 5 seconds and a phrase time limit of 3 seconds
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)  # Recognize the spoken word using Google's recognizer
                if "jarvis" in word.lower():  # Check if the wake word is spoken
                    speak("Yes?")  # Respond to the wake word
                    print("Jarvis Active..")
                    with sr.Microphone() as source:  # Use the microphone again for the next command
                        # Listen for the command with a timeout of 5 seconds and a phrase time limit of 5 seconds
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)  # Recognize the command using Google's recognizer
                        processCommand(command)  # Process the recognized command
        except sr.UnknownValueError:
            print("Could not understand audio")  # Handle case where the recognizer doesn't understand the audio
        except sr.RequestError as e:
            print(f"Could not request results; {e}")  # Handle request errors from the recognizer
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle any other exceptions
