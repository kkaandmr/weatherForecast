import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# OpenWeatherMap API key
API_KEY = ""# Change to your API_KEY

def send_email(subject, message, recipient_email):
    try:
        sender_email = "denemeddeneme9@gmail.com"  # Change to your email
        sender_password = "pnuo myae tdsd oeyp"  # Change to your password

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error while sending email:", e)

def get_weather(city_name, recipient_email):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def search_weather():
    city_name = city_entry.get()
    recipient_email = "denemeddeneme7@gmail.com"  # Change to recipient's email
    data = get_weather(city_name, recipient_email)
    if data['cod'] == '404':
        messagebox.showerror("Error", "City not found. Please enter a valid city name.")
    else:
        weather_desc = data['weather'][0]['description'].title()
        temp = round(data['main']['temp'])  # Round temperature to the nearest integer
        city_country = f"{data['name']}, {data['sys']['country']}"

        city_label.config(text=city_country)
        weather_desc_label.config(text=weather_desc)
        temperature_label.config(text=f"{temp}°C")

        if 'rain' in weather_desc.lower():
            weather_icon_url = "https://openweathermap.org/img/wn/09d.png"  # Rain icon
            send_email("Rainy Weather Alert", f"The weather in {city_name} is rainy.", recipient_email)
        else:
            weather_icon_url = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"

        try:
            response = requests.get(weather_icon_url)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 100), Image.LANCZOS)
            weather_icon = ImageTk.PhotoImage(img)
            weather_icon_label.config(image=weather_icon)
            weather_icon_label.image = weather_icon
        except Exception as e:
            print("Error:", e)

window = tk.Tk()
window.title("Weather App")

city_entry = tk.Entry(window, font=("Helvetica", 14))
city_entry.pack()

search_button = tk.Button(window, text="Search Weather", command=search_weather, font=("Helvetica", 14))
search_button.pack()

city_label = tk.Label(window, font=("Helvetica", 16, "bold"))
city_label.pack()

weather_desc_label = tk.Label(window, font=("Helvetica", 14))
weather_desc_label.pack()

temperature_label = tk.Label(window, font=("Helvetica", 14))
temperature_label.pack()

weather_icon_label = tk.Label(window)
weather_icon_label.pack()

window.mainloop()
