from django.urls import path
from .views import voice_to_text, speech_recognition, voice_control, loginPage, registerPage, logoutUser, text_editing
from .speech_editor import speech_editor


urlpatterns = [
    path('voice_to_text', voice_to_text, name='voice_to_text'),
    path('', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('speech_recognition/', speech_recognition, name='speech_recognition'),
    path('voice_control/', voice_control, name='voice_control'),
    path('text_editing/', text_editing, name='text_editing'),
    path('speech_editor/', speech_editor, name='speech_editor'),
]
