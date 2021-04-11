import pyttsx3 #text-to-speech conversion library in Python. Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.
import datetime
import wikipedia #pip install wikipedia
from playsound import playsound #ubuntu not support startfile() of os module so going with this
import webbrowser #all website open because of this
import smtplib #first enable less secure apps in google account it is used for mail
#import os #play music required this
import speech_recognition as sr
engine = pyttsx3.init('espeak') #espeak api for text to speach
voices = engine.getProperty('voices')
engine.setProperty('rate',150) #speed of speech
engine.setProperty('volume', 1) #volume low(0) and high(1) 
engine.setProperty('voice', voices[29].id)

#below loop will give information about voices
#count=0
#for voice in voices:
#    print("Voice:")
#    print(" - ID: %s" % voice.id)
#    print(" - Name: %s" % voice.name)
#    print(" - Languages: %s" % voice.languages)
#    print(" - Gender: %s" % voice.gender)
#    print(" - Age: %s" % voice.age)
#    print(" - %s" % count)   
#    count += 1


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good Morning" )
        
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        
    elif:
        speak("Good Evening")
        
    speak("How can i help you")
        
    

def takeCommand():
    #it takes microphone i/p input and returns string o/p
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # pause of number of seconds before completion of sentence
        r.energy_threshold = 400 #loudness of i/p sound for silent room are 0 to 100, and typical values for speaking are between 150 and 3500.
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-US')
        print(f"Usersaid: {query}\n") #F-strings are faster than the two most commonly used string formatting mechanisms, which are % formatting and str.format(). 
        
    except Exception as e:
        print(e)
        
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('Youremail','password') #sender email and password also less secure apps is required to enable
    server.sendmail('Receivers mail',to,content)
    server.close
        
if __name__ == "__main__":
    speak("hello sir")
    wishMe()
    while True: #putted it into comment because repeatedly listening
    #if 1:
        query = takeCommand().lower() #just because there should not mismatch b/w capital and small
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia wait for a moment...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=1)
            speak("According to wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
                
        elif 'google' in query:
            webbrowser.open("google.com")
                
        elif 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
                
        elif 'gmail' in query:
            webbrowser.open("gmail.com")
            
        elif 'play music' in query:
            #music_dir = '/home/dell/Downloads/Songs'
            #songs = os.listdir(music_dir)
            #mp3File=input('/home/dell/Downloads/Songs/songname.mp3')
            #print(songs) 
            #using playsound() because os.startfile not supporting
            playsound('/home/dell/Downloads/Songs/songname.mp3')
            #os.startfile(os.path.join(music_dir,songs[0])) #use random module to play random songs
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif 'send email to' in query:
            try:
                speak("What should i say")
                content = takeCommand() #takeCommand takes commands and returns in string
                to = "Receivers mail"
                sendEmail(to,content)
                speak("Email has been sent to")
            except Exception as e:
                print(e)
                speak("Sorry i can't send email")
        elif 'exit' in query:
            exit()
            break
        
        elif 'quit' in query:
            exit()
            break
