import speech_recognition as sr
import pyttsx3
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Function to recognize speech and return text
def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio_data = recognizer.listen(source)
        try:
            result_text = recognizer.recognize_google(audio_data)
            return result_text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results; check your network connection."

# Function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@csrf_exempt
def speech_editor(request):
    result_text = ""
    if request.method == "POST":
        result_text = listen_and_recognize()
        text_to_speech(result_text)
    return render(request, 'speech_editor.html', {'result_text': result_text})
