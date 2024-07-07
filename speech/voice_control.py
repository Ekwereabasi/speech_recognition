import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen_and_execute():
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        execute_command(command)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")
        engine.say("Sorry, I could not understand the audio")
        engine.runAndWait()
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        engine.say("Could not request results from Google Speech Recognition service")
        engine.runAndWait()

def execute_command(command):
    # Add your command handling logic here
    # For example, let's handle simple commands like "hello", "open browser", etc.
    if "hello" in command.lower():
        print("Hello! How can I help you?")
        engine.say("Hello! How can I help you?")
        engine.runAndWait()
    elif "open browser" in command.lower():
        print("Opening browser...")
        engine.say("Opening browser")
        engine.runAndWait()
        # Add your browser opening logic here
    else:
        print(f"Command '{command}' not recognized.")
        engine.say(f"Command '{command}' not recognized.")
        engine.runAndWait()
