#AI speech Assistant can do following functionality build on ubuntu 20.04
#play music or video
#tell weather or time
#open any website or software
#send mails
#search on wikipedia and read it
#play audiobooks
#open camera
#do calculations


import pyttsx3     #text-to-speech conversion library in Python. Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.
import datetime
import wikipedia   #pip install wikipedia
import playsound   #ubuntu not support startfile() of os module so going with this
import webbrowser  #all website open because of this
import smtplib     #first enable less secure apps in google account it is used for mail
import os          #play music required this
import pyowm       #open weather map for weather
import PyPDF2      #to read pdf
import speech_recognition as sr
import cv2         #to open camera for this install opencv-python library
import pyglet      #cv2 not allowing audio of video so we are going with polyget
import time        #for alarm
import inflect     #to convert 1,2,3...to first, second, third...

engine = pyttsx3.init('espeak') #espeak api for text to speach
voices = engine.getProperty('voices')
engine.setProperty('rate',175) #speed of speech
engine.setProperty('volume', 1) #volume low(0) and high(1) 
engine.setProperty('voice', 'en')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good Morning How can i help you" )     
        
    elif hour>=12 and hour<18:
        speak("Good Afternoon How can i help you")
        
    else:
        speak("Good Evening How can i help you")

def takeCommand():
    #it takes microphone i/p input and returns string o/p
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # pause of number of seconds before completion of sentence
        r.energy_threshold = 500 #loudness of i/p sound for silent room are 0 to 100, and typical values for speaking are between 150 and 3500.
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en')
        print(f"Usersaid: {query}\n") #F-strings are faster than the two most commonly used string formatting mechanisms, which are % formatting and str.format(). 
        
    except Exception as e:
        print(e)
        speak("Say that again please...")
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
    username='kamlesh'
    speak('hello' + username)
    wishMe()
    #while True: #putted it into comment because repeatedly listening
    if 1:
        query = takeCommand().lower() #just because there should not mismatch b/w capital and small   
        
        if 'wikipedia' in query:   
            speak('Searching Wikipedia wait for a moment...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=1)
            speak("According to wikipedia")
            print(results)
            speak(results)
            
        elif 'open website' in query:
           speak('Which website you want to open')
           query = takeCommand().lower()
           webbrowser.open(query+".com")
           
        #below manually checked each website  but above if condition dynamically do work     
        
        #elif 'open youtube' in query:
         #   webbrowser.open("youtube.com")
                
        #elif 'google' in query:
         #   webbrowser.open("google.com")
                
        #elif 'stackoverflow' in query:
         #   webbrowser.open("stackoverflow.com")
                
        #elif 'gmail' in query:
         #   webbrowser.open("gmail.com" 
            
        elif 'play music' in query:
            playsound.playsound('/home/dell/Downloads/Songs/Haan Main Galat - Love Aaj KalKartik, SaraPritamArijit SinghShashwat.mp3')
            
        elif 'play video' in query:
            vid_path="/home/dell/PythonPrograms/Extra/video.mp4"
            window=pyglet.window.Window()
            player = pyglet.media.Player()
            source = pyglet.media.StreamingSource()
            MediaLoad = pyglet.media.load(vid_path)
            player.queue(MediaLoad)
            player.play()
            @window.event
            def on_draw():
                if player.source and player.source.video_format:
                    player.get_texture().blit(50,50)
                    pyglet.app.run()
            
        elif 'open camera' in query:
            
            vid = cv2.VideoCapture(0)
            while(True):
                ret, frame = vid.read()  #capture the video frame by frame
                cv2.imshow('frame', frame)  # Display the resulting frame
                if cv2.waitKey(1) & 0xFF == ord('q'): #q button set for quit
                       break
                #below two statement will close camera window otherwise even after pressing q window will be stucked there will last frame
            vid.release()  #After the loop release the cap object
            cv2.destroyAllWindows()  # Destroy all the windows
            
        elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"Sir, the time is {strTime}")
                
        elif 'set alarm' in query:
            speak("What time you want to set alarm")
            speak("please tell hour")
            hour = takeCommand().lower()
            speak("please tell minutes")
            minute = takeCommand().lower()
            now = datetime.datetime.now()
            alarm_time = datetime.datetime.combine(now.date(), datetime.time(int(hour), int(minute), 0))
            time.sleep((alarm_time - now).total_seconds())
            speak("time to wake up" + username)
        
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
                
        elif 'weather' in query:
            owm = pyowm.OWM('765d13e14fac7f6abeef39eed9e0430d') #API key got from OpenWeatherMap website and imported pyown module
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place("surat,in")
            w = observation.weather
            temperature = w.temperature('celsius')
            print(temperature)
            speak(temperature)
            
        elif 'software' in query:
            speak('Which software you want to open')
            query = takeCommand().lower()
            if 'google chrome' in query :
               os.popen('/usr/bin/google-chrome')
               
            elif 'spyder' in query :
               os.popen('/usr/bin/spyder')   
         
            elif 'codeblocks' or 'code blocks'  in query :
               os.popen('/usr/bin/codeblocks')
               
            elif 'firefox' or 'fire fox' or 'mozila' in query :
               os.popen('/usr/bin/firefox')   
            
        elif 'read book' in query:            
            book = open('/home/dell/PythonPrograms/ProgrammingHero/bookname.pdf','rb') #rb means reading binary
            pdfReader = PyPDF2.PdfFileReader(book)
            pages = pdfReader.numPages #returns number of pages
            speaker = pyttsx3.init()
            #for i in range(7,pages) to read entire book
            page = pdfReader.getPage(7)
            text = page.extractText()
            speaker.say(text)
            speaker.runAndWait()
            
        elif 'do calculation' in query:
            speak("what do you want to perform addition or subtraction or multiplication or devision")
            operation=takeCommand().lower()
            i=1
            result=0
            a=0
            if(operation == 'addition'):
                while(1):
                    p = inflect.engine()
                    speak("give me"+p.ordinal(i)+'number') #not speaking properly like first second third...
                    a=str(a)
                    a=takeCommand().lower()
                    if('done' == a ):
                        break
                    result=result+int(a)
                    a=str(a)
                    i=i+1
                
            elif(operation == 'subtraction'):     
               speak('give a number') 
               a=takeCommand().lower()
               speak('what number you want to subtract from'+a)
               b=takeCommand().lower()
               result=int(a)-int(b)
               
            elif(operation == 'multiplication'):
                result=1
                while(1):
                        p = inflect.engine()
                        speak("give me"+p.ordinal(i)+'number') #not speaking properly like first second third...
                        a=str(a)
                        a=takeCommand().lower()
                        if('done' == a ):
                            break
                        result=result*int(a)
                        a=str(a)
                        print(result)
                        i=i+1    
                        
            elif(operation == 'division'): 
               result=1
               speak('give a number') 
               a=takeCommand().lower()
               speak('give a divisor for '+a)
               b=takeCommand().lower()
               result=int(a)/int(b)
            
            speak("result is" + str(result))    
              
        elif 'what you can do' in query:
            speak("Hello"+username)
            speak("i can do given operations like")
            speak("tell current time")
            speak("tell weather")
            speak("open camera")
            speak("play music or video")
            speak("play audiobook")
            speak("wait i can do more like")
            speak("set alarm")
            speak("do calculations")
            speak("open websites")
            speak("open softwares")
            speak("search information on wikipedia")
            speak("send mails")
            speak("welocome" + username)
            
        elif 'exit' in query:
            exit()
        # break #to comeout of loop of repeatedly asking on console
