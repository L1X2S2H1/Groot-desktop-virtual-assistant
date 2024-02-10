import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import sys 
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui
import requests
import time
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt 
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from grootui import Ui_GrootUi




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices'); 
#print(voices[0].id)
engine.setProperty('voices',voices[len(voices)-1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak(f"Good morning, its {tt}")
    elif hour>12 and hour<17:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("I am grooot . please tell me how can i help you.")


#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('grootai2023@gmail.com','LogiTech_8741' )
    server.sendmail('<grootprojectpy2122@gmail.com>',to, content)
    server.close()


#to tell news
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=d7394c96bb6e403190ccf92438c7061b'

    main_page = requests.get(main_url).json()
    #print (main_page)
    articles = main_page["articles"]
    #print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
           head.append(ar["title"])
    for i in range (len(day)):
           speak(f"today's {day[i]} news is: {head[i]}")

#to tell weather forecast
def weather():
    city_name, ok_pressed = QInputDialog.getText(None, 'City Name', 'Enter the name of the city:')
if ok_pressed:
    speak(f"You entered: {city_name}")
    api_key = "4488854187f35819f433bf04763f3cde"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response1=requests.get(complete_url)
    x = response1.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        deg = str(int(current_temperature-273.15))
        current_pressure = y["pressure"]
        pre = str(current_pressure)
        current_humidity = y["humidity"]
        hum=str(current_humidity)
        z = x["weather"]
        weather_description = z[0]["description"]
        wethr=str(weather_description)
        speak(f" Temperature is {deg} degree celcius , atmospheric pressure is {pre} mBar and humidity is {hum} percent and description is {wethr}")
    else:
        print(" City Not Found ")



class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()


#To convert voice to text
    def takecommand(self):  
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            #audio = r.listen(source,timeout=1,phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e :
            speak("Say that again please...")
            return"none"
        query = query.lower()
        return query


    def TaskExecution(self) :
        wish()
        while True:


            self.query = self.takecommand()


            #common tasks

            if "open notepad" in self.query:                                               #for notepad
                notepadpath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(notepadpath)

            elif "close notepad" in self.query:                                           #to close notepad
                speak("okay sir , closing notepad.")
                os.system("taskkill /f /im notepad.exe")

            elif "open 1 note" in self.query:                                             #for onenote
                os.system("start OneNote for Windows 10")

            elif "open command prompt" in self.query:                                     #for command prompt
                os.system("start cmd")

            elif "open camera" in self.query:                                            #for camera but there is some error
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break; 
                cap.release()
                cv2.destroyAllWindows()

            elif "ip address" in self.query:                                #for ip address
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif "wikipedia" in self.query:                                 #for wikipedia
                speak("searching wikipedia....")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query, sentences=4)
                speak("according to wikipedia")
                speak(results)
            # print(results)

            elif "open youtube" in self.query:                              #for youtube
                webbrowser.open("www.youtube.com")

            elif "open instagram" in self.query:                            #for Instagram
                webbrowser.open("www.instagram.com")

            elif "open amazon" in self.query:                               #for amazon
                webbrowser.open("www.amazon.in")

            elif "open flipkart" in self.query:                              #for flipkart
                webbrowser.open("www.flipkart.com")

            elif "open google" in self.query:                                #for google
                speak("sir , what should i search on google.")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "send whatsapp message" in self.query:                      #for sending message on whatsapp but it should be login on the web
                speak("Sir, please enter phone number")
                phno = input("Enter the no. = ")
                speak("Sir , tell me what shout i type in the message.")
                messg = self.takecommand().lower()
                kit.sendwhatmsg_instantly(phno,messg)

            elif "play youtube" in self.query:                             #play any video on yt
                speak("Sir, what should i play. ")
                srh = self.takecommand().lower()
                kit.playonyt(srh)


            elif "send email" in self.query:                                   # to send email but having error in login
                try:
                    speak("sir , please enter the email. ")
                    to =input("Enter the email : ")
                    speak("what should i say sir ?")
                    content = self.takecommand().lower()                          
                    sendEmail(to,content)
                    speak("Email has been sent .")

                except Exception as e:
                    print(e)
                    speak("sorry sir, i am not able to sent this email .")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "sleep now" in self.query:                                             #to crack a joke
                speak("thanks for using me sir , have a good day.")
                sys.exit()

            elif "shut down the system" in self.query:                                   #to shut down the system
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:                                      #to restart the system
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:                                        #to sleep the system
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


            elif "hello" in self.query or "hey" in self.query:
                speak("hello sir , may i help you with something.")


            elif "how are you" in self.query:
                speak("i am fine sir , what about you.")

            
            elif "thank you" in self.query or "thanks" in self.query:
                speak("it's my pleasure sir.")

            
            elif "who are you" in self.query:
                speak("I am an artificial intelligence . And I was created to make your work easier. ")


            elif "who made you" in self.query or "who is your creator" in self.query:
                speak("I am a result of joint efforts of laksh , ayush and himanshu")

            elif "the time" in self.query:                                               #To tell the current time
                strTime =datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir ,the time is  {strTime}")

            elif "switch the window" in self.query:                                       #To switch the window.
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")


            elif "tell me news" in self.query:                                          #to tell the news
                speak("please wait sir , fetching the latest news")
                news()


            elif "where i am" in self.query or "where we are" in self.query:                    #to tell current location
                speak("wait sir, let me check")
                try:
                    ipAddrs = requests.get('https://api.ipify.org').text
                    print(ipAddrs)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAddrs+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(f"sir i am not sure , but we are in {city} city of  of {country} .")
                except Exception as e:
                    speak("sorry sir , due to network issue i am not able to find where we are .")
                    pass


            elif "instagram profile" in self.query or "profile on instagram" in self.query:               #to check instagram profile.
                speak("sir please enter the user name .")
                name = input("Enter username here : ")
                webbrowser.open(f"www.instagram.com/{name}")
                time.sleep(5)
                speak("sir here is your instagram profile. now i am ready for next command")


            elif "weather" or "wheather" in self.query:
                weather()

                



            elif "no thanks" in self.query:
                speak("Thanks for using me sir , have a good day.")
                sys.exit()


startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self) :
        super().__init__()
        self.ui = Ui_GrootUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D:/gui/fram(1).jpg")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/gui/3nOo.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/gui/BigheartedVagueFoal-size_restricted.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/gui/—Pngtree— frames technology futuristic interface_5479025.png")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/gui/VJl.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/gui/f889323d87ae92dbd5da3b1193708dc3.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date =QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
groot = Main()
groot.show()
sys.exit(app.exec_())