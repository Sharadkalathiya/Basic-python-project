import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, I am having trouble connecting to the internet.")
    return ""

# Function to send an email
def send_email(to_email, subject, message):
    try:
        from_email = "sharadkalathiya2210@gmail.com"  # Replace with your email
        password = "sharad1727"  # Replace with your password
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        speak("Email sent successfully!")
    except Exception as e:
        speak("Failed to send email.")
        print(f"Error: {e}")

# Function to get weather updates
def get_weather(city):
    try:
        api_key = "a0e0f51db5c4129aaf4d43da24cb9926"  # Replace with your OpenWeather API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        if weather_data['cod'] == 200:
            weather = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            weather_info = f"The weather in {city} is {weather} with a temperature of {temp}°C."
            speak(weather_info)
            return weather_info
        else:
            speak("City not found.")
            return "City not found."
    except Exception as e:
        speak("Failed to get weather updates.")
        print(f"Error: {e}")
        return "Error in getting weather updates."

# Function to set a reminder
def set_reminder(reminder_text, time_minutes):
    speak(f"Reminder set for {time_minutes} minutes from now.")
    def reminder_task():
        threading.Timer(time_minutes * 60, lambda: speak(f"Reminder: {reminder_text}")).start()
    reminder_task()

# Function to answer general knowledge questions
def answer_question(query):
    try:
        response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
        data = response.json()
        answer = data.get('AbstractText', "Sorry, I couldn't find an answer.")
        speak(answer)
        return answer
    except Exception as e:
        speak("Failed to get the answer.")
        print(f"Error: {e}")
        return "Error in getting the answer."

# GUI Class
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Assistant")
        self.root.geometry("600x400")
        self.root.config(bg="#2c3e50")

        # GUI Elements
        self.title_label = tk.Label(root, text="Advanced Voice Assistant", font=("Arial", 24), bg="#2c3e50", fg="white")
        self.title_label.pack(pady=20)

        self.speak_button = tk.Button(root, text="Speak", command=self.listen_command, font=("Arial", 18), bg="#27ae60", fg="white")
        self.speak_button.pack(pady=20)

        self.output_label = tk.Label(root, text="", font=("Arial", 14), bg="#2c3e50", fg="white", wraplength=500)
        self.output_label.pack(pady=20)

    def listen_command(self):
        query = recognize_speech()
        self.output_label.config(text=f"You said: {query}")
        if "email" in query:
            self.handle_email()
        elif "weather" in query:
            self.handle_weather()
        elif "reminder" in query:
            self.handle_reminder()
        elif "question" in query or "answer" in query:
            self.handle_question(query)
        else:
            speak("Sorry, I can't help with that yet.")

    def handle_email(self):
        speak("Who is the recipient?")
        to_email = recognize_speech()
        speak("What is the subject?")
        subject = recognize_speech()
        speak("What is the message?")
        message = recognize_speech()
        send_email(to_email, subject, message)

    def handle_weather(self):
        speak("Which city do you want the weather for?")
        city = recognize_speech()
        weather_info = get_weather(city)
        self.output_label.config(text=weather_info)

    def handle_reminder(self):
        speak("What should I remind you about?")
        reminder_text = recognize_speech()
        speak("In how many minutes?")
        time_minutes = recognize_speech()
        try:
            time_minutes = int(time_minutes)
            set_reminder(reminder_text, time_minutes)
        except ValueError:
            speak("I couldn't understand the time. Please try again.")

    def handle_question(self, query):
        speak("Let me find that for you.")
        answer = answer_question(query)
        self.output_label.config(text=answer)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
