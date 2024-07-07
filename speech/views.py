from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
import speech_recognition as sr
from django.http import HttpResponse
from .speech_editor import listen_and_recognize, text_to_speech
from .voice_control import listen_and_execute
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pyttsx3
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required


engine = pyttsx3.init()

# @unauthenticated_user
@login_required
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'speech/register.html', context)

# @unauthenticated_user
@login_required
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('voice_to_text')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'speech/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def voice_to_text(request):
    if request.method == 'POST':
        min_frequency = int(request.POST.get('min_frequency', 0))
        max_frequency = int(request.POST.get('max_frequency', 10000))
        recognizer = sr.Recognizer()
        with sr.Microphone(sample_rate=44100, chunk_size=1024) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return render(request, 'speech/result.html', {'text': text})
        except sr.UnknownValueError:
            return render(request, 'speech/result.html', {'error': 'Could not understand audio'})
        except sr.RequestError as e:
            return render(request, 'speech/result.html', {'error': f'Request failed; {e}'})
    return render(request, 'speech/voice_to_text.html')

@login_required(login_url='login')
def speech_recognition(request):
    recognized_text = None
    if request.method == 'POST':
        recognized_text = listen_and_recognize()
        if recognized_text:
            text_to_speech(recognized_text)
    return render(request, 'speech/speech_recognition.html', {'recognized_text': recognized_text})

@login_required(login_url='login')
def voice_control(request):
    if request.method == 'POST':
        listen_and_execute()
    return render(request, 'speech/voice_control.html')

@login_required(login_url='login')
def text_editing(request):
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            with open('edited_text.txt', 'r') as file:
                original_text = file.read().strip()
            result = perform_text_editing(command)
            return render(request, 'speech/text-editing.html', {'original_text': original_text, 'command': command, 'result': result})
        except sr.UnknownValueError:
            return render(request, 'speech/text-editing.html', {'error': 'Could not understand audio'})
    return render(request, 'speech/text-editing.html')

def perform_text_editing(command):
    if "append" in command:
        append_text = command.replace("append", "").strip()
        with open('edited_text.txt', 'a') as file:
            file.write(append_text + '\n')
        return f"Appended: {append_text}"
    elif "replace" in command:
        replace_text = command.replace("replace", "").strip()
        with open('edited_text.txt', 'a') as file:
            file.write(replace_text + '\n')
        return f"Appended: {replace_text}"
    elif "remove" in command:
        with open('edited_text.txt', 'w') as file:
            file.write('')
        return "Text removed"
    else:
        return "No recognized command"
