import subprocess
import pyttsx3
import requests
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia

from threading import Thread

# ---------------- Object Initialization ----------------
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')  # Windows Speech API

# Configure Voice Engine
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)  # Select first voice
    engine.setProperty('rate', 175)  # Adjust speed
    engine.setProperty('volume', 1.0)  # Set volume to max
else:
    print("No voices found! Check TTS installation.")

# ---------------- Variables ----------------
is_awake = True  # Bot status
today = date.today()
file_exp_status = False
files = []
path = ''

# ---------------- Functions ----------------


def reply(audio):
    """Speaks and prints the given message."""
    print(f"Assistant: {audio}")  # Debugging output
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-Speech Error: {e}")

def wish():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        reply("Good Morning!")
    elif 12 <= hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am your assistant. How may I help you?")


# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500 
    r.dynamic_energy_threshold = False

def record_audio():
    """Records audio and converts it to text using speech recognition."""
    with sr.Microphone() as source:
        print("Listening for command...")  
        r.adjust_for_ambient_noise(source, duration=1)  # Adjusts to noise
        audio = r.listen(source, phrase_time_limit=5)  # Listen for 5 seconds
        
        try:
            voice_data = r.recognize_google(audio).lower()
            print(f"Recognized Voice: {voice_data}")  # Debugging output
            return voice_data
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return ""
        except sr.RequestError:
            reply('Speech recognition service is unavailable. Check your internet connection.')
            return ""

def respond(voice_data):
    """Processes the recognized voice command."""
    global file_exp_status, files, is_awake, path

    print(f"Processing command: {voice_data}")  # Debugging output

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return



    # STATIC CONTROLS
    if 'hello' in voice_data:
        wish()
    elif 'your name' in voice_data:
        reply('My name is Proton!')
    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))
    elif 'time' in voice_data:
        reply(datetime.datetime.now().strftime("%H:%M:%S"))
    elif 'search for' in voice_data:
        query = voice_data.replace("proton search for", "").strip()
        reply(f"Searching for {query}")
        webbrowser.open(f"https://google.com/search?q={query}")
    elif 'location' in voice_data:
        reply("Which place are you looking for?")
        place = record_audio()
        if place:
            reply("Locating...")
            webbrowser.open(f"https://www.google.com/maps/place/{place}/")
            reply("Here is the location.")
    elif 'bye' in voice_data:
        reply("Goodbye! Have a nice day.")
        is_awake = False
    elif 'exit' in voice_data or 'terminate' in voice_data:
        reply("Exiting successfully.")
        sys.exit()

    elif 'launch system' in voice_data:
        global gesture_process
        reply("Launching Gesture Recognition System...")
        try:
           gesture_process = subprocess.Popen(["python", "C:\Final_Project\src\Gesture_Controller.py"])  # Adjust filename if needed
           reply("Gesture Recognition System started successfully.")
        except FileNotFoundError:
            reply("Gesture Recognition System script not found!")
        except Exception as e:
            reply(f"Error launching the Gesture Recognition System: {e}") 

    elif 'stop system' in voice_data:
        stop_gesture_system()  # Stop the launched system when this command is given           
 
    # DYNAMIC CONTROLS
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied.')
    elif 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted.')

    # File Navigation (Default Folder: C://)
    elif 'list' in voice_data:
        path = 'C://'
        files = listdir(path)
        file_exp_status = True
        reply('These are the files in your root directory:')
        print("\n".join(files))  # Debugging output
    elif file_exp_status:
        if 'open' in voice_data:
            try:
                index = int(voice_data.split()[-1]) - 1
                selected_file = files[index]
                new_path = join(path, selected_file)
                if isfile(new_path):
                    os.startfile(new_path)
                    reply(f"Opened {selected_file}")
                else:
                    path = new_path + "//"
                    files = listdir(path)
                    reply("Opened folder successfully.")
            except (IndexError, ValueError, PermissionError):
                reply("Unable to open the file or folder.")
        elif 'back' in voice_data:
            if path == 'C://':
                reply('Already at the root directory.')
            else:
                path = "//".join(path.split("//")[:-2]) + "//"
                files = listdir(path)
                reply('Moved back.')
    else:
        reply("I'm not programmed to do that!")

def stop_gesture_system():
    global gesture_process
    if gesture_process:
        reply("Stopping the Gesture Recognition System...")
        gesture_process.terminate()  # Terminate the process
        reply("Gesture Recognition System stopped.")
    else:
        reply("No Gesture Recognition System is currently running.")

def open_application(voice_data):
    if 'notepad' in voice_data:
        os.system('notepad')
        reply("Notepad Opening...")
    elif 'calculator' in voice_data:
        os.system('calc')
        reply("Calculator Opening...")
    elif 'cmd' in voice_data or 'cmd' in voice_data:
        os.system("start cmd")
    elif 'chrome' in voice_data:
        os.system("start chrome")
    elif 'control panel' in voice_data:
        os.system("control")
    elif 'this pc' in voice_data or 'my computer' in voice_data:
          reply("Opening This PC...")
          os.system('explorer shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}')
    else:
        reply("I'm not programmed to do that!")


def control_volume(voice_data):
    if 'increase volume' in voice_data:
        for _ in range(5):
            pyautogui.press("volumeup")
    elif 'decrease volume' in voice_data:
        for _ in range(5):
            pyautogui.press("volumedown")
    elif 'mute' in voice_data:
        pyautogui.press("volumemute") 
    else:
        reply("I'm not programmed to do that!")        

def system_control(voice_data):
    if 'shutdown' in voice_data:
        reply("Shutting down the system.")
        os.system("shutdown /s /t 5")
    elif 'restart' in voice_data:
        reply("Restarting the system.")
        os.system("shutdown /r /t 5")
    elif 'sleep' in voice_data:
        reply("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  
    else:
        reply("I'm not programmed to do that!")       

def open_website(voice_data):
    if 'youtube' in voice_data:
        webbrowser.open("https://www.youtube.com")
    elif 'facebook' in voice_data:
        webbrowser.open("https://www.facebook.com")
    elif 'twitter' in voice_data:
        webbrowser.open("https://www.twitter.com")
    elif 'instagram' in voice_data:
        webbrowser.open("https://www.instagram.com")
    elif 'google' in voice_data:
        webbrowser.open("https://www.google.com")
    elif 'github' in voice_data:
        webbrowser.open("https://www.github.com")
    else:
        reply("Website not recognized. Please try again.")

     

# ---------------- Driver Code ----------------
print("Starting Proton Voice Assistant...")
wish()

while True:
    try:
        voice_data = record_audio()
        if 'proton' in voice_data:
            respond(voice_data)
        elif 'open website' in voice_data:  # Added to check for website opening commands
            open_website(voice_data)
        elif 'open' in voice_data:
            open_application(voice_data)
        elif 'increase' in voice_data or 'decrease' in voice_data or 'mute' in voice_data:
            control_volume(voice_data)
        elif 'shutdown' in voice_data or 'restart' in voice_data or 'sleep' in voice_data:
             system_control(voice_data)

        
    except SystemExit:
        break
    except Exception as e:
        print(f"Error: {e}")
