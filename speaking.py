from email.mime import audio
from numpy import void
import pyttsx3
import speech_recognition as sr

speaking  = pyttsx3.init()
voice = speaking.getProperty('voices')
speaking.setProperty('voice',voice[1].id)


def speak(audio):
    speaking.say(audio)
    speaking.runAndWait()




# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Talk")
#     audio_text = r.listen(source)
#     print("Time over, thanks")
#     try:
#         print("Text: "+ r.recognize_google(audio_text))
#     except:
#         print("Sorry, I did not get that")


def get_text_vi():
    for i in range(3):
        text_vi = get_voice_vi()
        if text_vi:
            test(text_vi)
            return text_vi.lower()
        # elif i < 2:
        #     speak("Bot không nghe rõ. Bạn nói lại được không!")
        else:
            return 0
    return 0

def get_voice_vi():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Me: ", end='')
        audio_vi = r.listen(source, phrase_time_limit=5)
        try:
            text_vi = r.recognize_google(audio_vi, language="vi-VN")
            # print(text_vi, end = '')
            # print("")
            return text_vi
        except:
            print("")
            return 0

def test(text_vi):
    if "chào" in text_vi:
        speak("xin chào bạn")
    else:
        print("jn")



get_voice_vi()
get_text_vi()
