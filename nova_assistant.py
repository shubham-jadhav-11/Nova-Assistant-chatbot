import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import random
import platform
import psutil
import sys
import subprocess
import smtplib
import time
import requests

class NovaAI:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.listener = sr.Recognizer()
        self.greet_user()

    def speak(self, text):
        print(f"Nova: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.listener.adjust_for_ambient_noise(source)
                audio = self.listener.listen(source, timeout=5)
                command = self.listener.recognize_google(audio)
                command = command.lower()
                print(f"You said: {command}")
                return command
        except Exception as e:
            # print(e)
            return ""

    def greet_user(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon!"
        elif 17 <= hour < 22:
            greeting = "Good evening!"
        else:
            greeting = "Hello!"
        self.speak(f"{greeting} I'm Nova AI, your desktop assistant.")

    def tell_time(self):
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {time_str}")

    def tell_date(self):
        date_str = datetime.datetime.now().strftime("%A, %d %B %Y")
        self.speak(f"Today's date is {date_str}")

    def open_website(self, url):
        self.speak(f"Opening {url}")
        webbrowser.open(url)

    def tell_joke(self):
        jokes = [
            "Why did the computer get cold? Because it left its Windows open.",
            "I'm reading a book on anti-gravity. It's impossible to put down.",
            "Why don't scientists trust atoms? Because they make up everything.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the cell phone wearing glasses? Because it lost its contacts."
        ]
        joke = random.choice(jokes)
        self.speak(joke)

    def system_info(self):
        sys_info = platform.uname()
        self.speak(f"You are using a {sys_info.system} system with a {sys_info.processor} processor.")

    def battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            self.speak(f"Battery is at {percent} percent.")
        else:
            self.speak("Sorry, I couldn't get battery information.")

    def play_music(self, path):
        if os.path.exists(path):
            self.speak("Playing your music")
            os.startfile(path)
        else:
            self.speak("Music file not found.")

    def search_wikipedia(self, topic):
        try:
            result = wikipedia.summary(topic, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(result)
        except:
            self.speak("I couldn't find anything about that.")

    def send_email(self, to, subject, body):
        # Requires setup: SMTP server, login, password
        # Replace below placeholders with your email credentials
        sender_email = "youremail@example.com"
        sender_password = "yourpassword"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to, message)
            server.quit()
            self.speak("Email has been sent!")
        except Exception as e:
            print(e)
            self.speak("Sorry, I was unable to send the email.")

    def open_application(self, app_name):
        # Add paths for your common apps here
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            # Add more apps with full path or command
        }
        if app_name in apps:
            path = apps[app_name]
            try:
                subprocess.Popen(path)
                self.speak(f"Opening {app_name}")
            except Exception as e:
                print(e)
                self.speak(f"Failed to open {app_name}")
        else:
            self.speak(f"I don't know how to open {app_name}")

    def google_search(self, query):
        self.speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def small_talk(self, command):
        responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm an AI, so I don't have feelings, but thanks for asking!",
            "what's your name": "I'm Nova, your personal assistant.",
            "thank you": "You're welcome!",
            "thanks": "Anytime!"
        }
        for key, response in responses.items():
            if key in command:
                self.speak(response)
                return True
        return False

    def simple_calculator(self, expression):
        # Simple calculation support for +, -, *, /
        try:
            result = eval(expression)
            self.speak(f"The result is {result}")
        except:
            self.speak("Sorry, I couldn't calculate that.")

    def get_weather(self, city):
        # Free API key needed from OpenWeatherMap
        api_key = "YOUR_API_KEY_HERE"  # Replace with your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] != 200:
                self.speak("City not found.")
                return
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            self.speak(f"Current weather in {city} is {weather} with temperature {temp} degrees Celsius.")
        except:
            self.speak("Sorry, I couldn't get the weather information.")

    def respond(self, command):
        if not command:
            return

        if self.small_talk(command):
            return

        if "time" in command:
            self.tell_time()
        elif "date" in command:
            self.tell_date()
        elif "open youtube" in command:
            self.open_website("https://www.youtube.com")
        elif "open google" in command:
            self.open_website("https://www.google.com")
        elif "open github" in command:
            self.open_website("https://www.github.com")
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            self.search_wikipedia(topic)
        elif "joke" in command:
            self.tell_joke()
        elif "battery" in command:
            self.battery_status()
        elif "system" in command:
            self.system_info()
        elif "play music" in command:
            music_path = "D:\\Music\\sample.mp3"  # change this to your file path
            self.play_music(music_path)
        elif "open" in command and "application" in command:
            # example: "open calculator application"
            app = command.replace("open", "").replace("application", "").strip()
            self.open_application(app)
        elif "send email" in command:
            # basic example: "send email to john@example.com subject Hello body How are you"
            try:
                parts = command.split(" ")
                to_index = parts.index("to") + 1
                subj_index = parts.index("subject") + 1
                body_index = parts.index("body") + 1
                to = parts[to_index]
                subject = parts[subj_index]
                body = " ".join(parts[body_index:])
                self.send_email(to, subject, body)
            except:
                self.speak("Please provide email details as: send email to [email] subject [subject] body [message]")
        elif "google search" in command:
            query = command.replace("google search", "").strip()
            self.google_search(query)
        elif "calculate" in command:
            expression = command.replace("calculate", "").strip()
            self.simple_calculator(expression)
        elif "weather" in command:
            # example: "weather in Mumbai"
            city = command.replace("weather", "").replace("in", "").strip()
            self.get_weather(city)
        elif "exit" in command or "quit" in command or "stop" in command:
            self.speak("Goodbye!")
            sys.exit()
        else:
            self.speak("Sorry, I didn't understand that. Could you repeat?")

    def run(self):
        while True:
            command = self.listen()
            if command:
                self.respond(command)

if __name__ == "__main__":
    assistant = NovaAI()
    assistant.run()
