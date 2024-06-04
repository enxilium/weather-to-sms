import requests
import smtplib
import ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

city = "Mississauga"
url = "https://www.google.com/search?q="+"weather"+city+"tomorrow"
html = requests.get(url).content
recipients = ["yourOwnPhoneNumber'sEmail@serviceprovider.com"]
port = 465
password = "nbtlirrzprdkqxlw"
weatherConditions = {
    "Partly Sunny": "⛅️",
    "Scattered Thunderstorms": "⛈️",
    "Thunderstorm": "⛈️",
    "Chance of Storm": "⛈️",
    "Chance of Thunderstorm": "⛈️",
    "Storm": "⛈️",
    "Sunny": "☀️",
    "Mostly Sunny": "☀️",
    "Partly Cloudy": "⛅️",
    "Mostly Cloudy": "⛅️",
    "Cloudy": "☁️",
    "Overcast": "⛈️",
    "Rain": "🌧️",
    "Light Rain": "🌧️",
    "Chance of Rain": "🌧️",
    "Showers": "☔️",
    "Scattered Showers": "☔️",
    "Freezing Drizzle": "☔️❄️",
    "Snow": "❄️",
    "Flurries": "❄️",
    "Icy": "❄️",
    "Chance of Snow": "❄️",
    "Hail": "❄️",
    "Light Snow": "🌨️",
    "Snow Showers": "🌨️",
    "Rain and Snow": "🌨️🌧️",
    "Sleet": "🌨️🌧️",
    "Fog": "🌫️",
    "Mist": "🌫️",
    "Dust": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Clear": "☀️"
}

# getting raw data
soup = BeautifulSoup(html, 'html.parser')

# parsing for weather div
weather = soup.find('div', class_ = 'BNeawe tAd8D AP7Wnd').text.split('\n')

# parsing for individual data
day = weather[0][0:3]
skies = weather[1]
temp = re.sub(r'[^A-Za-z0-9 ]+', '', weather[2])

# assebling message
msg = f"""{skies} {weatherConditions[skies]}
{temp}"""

print(msg)

email_message = MIMEMultipart()
email_message['From'] = "arxarobot@gmail.com"
email_message['To'] = ",".join(recipients)
email_message['Subject'] = f"{day}"

body = MIMEText(msg)
email_message.attach(body)

# login to email server
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
    server.login("arxarobot@gmail.com", password)

    # send email
    for recipient in recipients:
        server.send_message(email_message, "arxarobot@gmail.com", recipient)