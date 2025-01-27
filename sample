import speech_recognition as sr
from playsound import playsound

r = sr.Recognizer()
while True:
    duration=0.2
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
        print("Res is ",response)
    except:
        
        response = 'N'
        print("Res is1 ",response)
