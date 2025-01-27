from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
duration=10
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=10)
    playsound('speak.mp3')
    audio = r.listen(source, phrase_time_limit=duration)
    #audio = r.listen(source, timeout=10)
    audio = r.listen(source)
try:
    response = r.recognize_google(audio,language="en-US")
    print("Res is ",response)
except:
    
    response = 'N'
    print("Res is1 ",response)
