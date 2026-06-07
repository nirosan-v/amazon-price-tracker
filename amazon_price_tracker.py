import requests
from bs4 import BeautifulSoup
import datetime
import os
import smtplib
from email.message import EmailMessage

# Scrape Amazon product page
url = requests.get(
    "https://www.amazon.co.uk/Waterpik-Cordless-Advanced-Bathrooms-WP-580UK/dp/B0CM44DSFC/ref=sr_1_9?sr=8-9",
    timeout=5,
).text
soup = BeautifulSoup(url, "html.parser")

# Extract the product price
symbol = soup.find("span", class_="a-price-symbol").text
whole = soup.find("span", class_="a-price-whole").text
fraction = soup.find("span", class_="a-price-fraction").text
price = float(whole + fraction)

# Get current date and time
now = datetime.datetime.now()
time = now.strftime("%H:%M:%S")
date = now.strftime("%d-%m-%Y")

# Store price history in CSV file
os.chdir("your_csv_location")
with open("water_flosser.csv", "a") as f:
    f.write(f"{time},{date},{price}\n")

# Send email alert if product price is below £70
def send_email(price):
    msg = EmailMessage()
    msg.set_content(
        f"Price has dropped to {symbol}{price}. Buy it here: https://www.amazon.co.uk/Waterpik-Cordless-Advanced-Bathrooms-WP-580UK/dp/B0CM44DSFC "
    )
    msg["Subject"] = "Water flosser price alert!"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "recipient@email.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("your_email@gmail.com", "your_app_password")
        smtp.send_message(msg)


if price < 70:
    send_email(price)
