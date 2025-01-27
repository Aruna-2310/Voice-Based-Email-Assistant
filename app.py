import speech_recognition as sr
from playsound import playsound
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting noise ")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    playsound('speak.mp3')
    recorded_audio = recognizer.listen(source, timeout=4)
    print("Done recording")

try:
    print("Recognizing the text")
    text = recognizer.recognize_google(
            recorded_audio, 
            language="en-US"
        )

    print("Decoded Text : {}".format(text))

except Exception as ex:

    print(ex)


#sr.Microphone.list_microphone_names()