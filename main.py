from pymongo import MongoClient
import smtplib
import time
from pymongo.server_api import ServerApi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

stringConnx = os.getenv('CONN_STRING')
client = MongoClient(stringConnx, server_api=ServerApi('1'))
database = client["Abhedya2k24"]


def gen_email(user):
  sender = "mehul.213amb@gmail.com"
  password = "kdad rjtn bcfs uica"
  subject = f"Login to play Abhedya - successful registration"
  html = f"""
      <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gaze Upward: Explore the Cosmic Canvas</title>
            <style>
                body {{
                    background: #0f202d;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    color: white;
                    justify-content: center;
                    align-items: center;
                }}

                .container {{
                    background: #1e3449;
                    border-radius: 10px;
                    padding: 40px;
                    max-width: 800px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                }}

                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }}

                .title {{
                    font-size: 2.5em;
                    text-align: center;
                    color: #d5e4ff;
                    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                }}

                .images {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100vw;
                }}

                .image {{
                    width: 70px;
                }}

                .content {{
                    line-height: 1.5;
                    margin-bottom: 20px;
                    color: #ffffff !important;
                }}

                .box {{
                    background: #2d343c;
                    border-radius: 5px;
                    padding: 20px;
                    margin-bottom: 20px;
                }}


                .list {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}

                .list-item {{
                    margin-bottom: 5px;
                }}

                a:hover {{
                    background-color: #d5e4ff;
                }}

                .button {{
                    background: linear-gradient(to right, #3a75ff, #3254db);
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease-in-out;
                }}

                .button:hover {{
                    transition: all 0.3s ease-in-out;
                    background: linear-gradient(to right, #3254db, #4a90e2);
                }}
            </style>
        </head>
        <body>
        <div class="container">
            <div class="header">
                <h1 class="title">Abhedya: The Biggest Online Cryptic Hunt of NITH!</h1>
            </div>
            <div class="images">
                <div class="image-container">
                    <img class="image" src="https://i.imgur.com/XoARgYd.png" alt="Constellation">
                </div>
                <div class="image-container">
                    <img class="image" width="100px" src="https://i.imgur.com/DMlETCl.png" alt="Nebula">
                </div>
            </div>
            <div class="content">
                <h1>Hi! {user["username"]}</h1>
                <p style="color: white;">You registered for Abhedya 2k24. \nTo login and play Abhedya, click the following button.</p>
                <a href="http://abhedya.istenith.com/user/login/{user["loginLink"]}">
                  <button class="button">Play Now!</button>
                </a>
                <br><br>
                If the button doesn't work, copy and paste the following link in your browser window and hit enter.<br>
                http://abhedya.istenith.com/user/login/{user["loginLink"]}
            </div>
        </div>
      </body>
      </html>
    """

  recipient = user["email"]

  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = recipient

  htmlPart = MIMEText(html, 'html')

  msg.attach(htmlPart)

  return msg.as_string()

def main():

    while True:
        print("out of sleep")
        users = list(database['users'].find({"emailSent": False}))
        sender = "prodyogiki.iste@gmail.com"
        password = "ivwk fusm tmon tsty"

        if len(users) > 0:

            print('users found with unsent emails')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                print("logged in server")

                for user in users:
                    email_to_send = gen_email(user)
                    print(user)

                    try:
                        smtp_server.sendmail("prody@istenith.com", user["email"], email_to_send)
                        print('mail sent')
                        database['users'].find_one_and_update({"email": user["email"]}, {"$set": {"emailSent": True}})
                    except:
                        print('###ERR couldnt send mail to {}'.format(user["username"]))

            # After sending all mails
            print('cleared queue')
        else:
            print("No pending emails")
        # wait 30 seconds before sending email again
        print("sleeping for 15 seconds")
        time.sleep(15)


main()