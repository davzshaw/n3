import base64
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from dotenv import load_dotenv

path = "storage/"

def sendAlert(toEmail, isCrying, temperature, soundBase64):
    load_dotenv()
    fromEmail = os.environ.get("EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    subject = "Emergency: Check on Your Baby"
    body = f"We have detected that your baby is {'crying' if isCrying else 'not crying'} and has a temperature of {temperature:.1f} Celsius degrees. Please check on them!"

    message = MIMEMultipart()
    message['From'] = fromEmail
    message['To'] = toEmail
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    if soundBase64:
        try:
            soundData = base64.b64decode(soundBase64)
            audio = MIMEAudio(soundData)
            audio.add_header('Content-Disposition', 'attachment', filename='alert_sound.wav')
            message.attach(audio)
        except base64.binascii.Error as e:
            print(f"Error decoding base64 audio: {e}")
            return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromEmail, password)

        server.sendmail(fromEmail, toEmail, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def sendEmail(crying=True, temperature=30):
    try:
        
        url = "https://undefinedprojectbackend.onrender.com/email/send"
        payload = {
            "to":"juandis0246@gmail.com",
            "subject":"Wannacry Alert",
            "body":f"""
WE HAVE YOU DETECTED YOUR LITTLE ANGEL IS IN RISK
Temperature: {temperature}°C
Crying: {'Yes' if crying else 'No'}"""
        }
        requests.post(url,payload)
        return "200"
        
    except:
        return "500"

def base64ToFile(filenameOrigin="sound.txt", filenameOutput="sound.wav"):
    
    try:    
        if not os.path.exists(path):
            os.makedirs(path)
            
        with open(path+filenameOrigin, "r") as file:
            base64Text = file.read()
            
            
        fileData = base64.b64decode(base64Text)
        
        with open(path+filenameOutput, 'wb') as file:
            file.write(fileData)
        return "200"
    except:
        return "500"

def fileToBase64(filenameOrigin="sound.wav", filenameOutput="sound.txt"):
    try:
        filePath = os.path.join(path, filenameOrigin)

        if not os.path.exists(filePath):
            raise FileNotFoundError(f"No such file: '{filePath}'")

        with open(filePath, 'rb') as file:
            fileData = file.read()
            
        base64String = base64.b64encode(fileData).decode('utf-8')
        
        with open(os.path.join(path, filenameOutput), "w") as file:
            file.write(base64String)
        return base64String
    except:
        return "500"

def deleteFiles(extension=".txt"):
    try:    
        if not os.path.exists(path):
            raise FileNotFoundError(f"No such directory: '{path}'")
        
        for fileName in os.listdir(path):
            if fileName.endswith(extension):
                filePath = os.path.join(path, fileName)
                
                with open(filePath, "w") as file:
                    file.write("deleted")
        return "200"
    except:
        return "500"
                
def readFiles(filename = "datetime.txt", binary = False):
    try:
        readingType = "r" if not binary else "rb"
        with open(path+filename, readingType) as file:
            return file.read()
        return "200"
    except Exception as e:
        return f"500: {str(e)}"

def writeFiles(content, filenameOutput):
    try:
        with open(path+filenameOutput, "w") as file:
            file.write(content)
        return "200"
    except:
        return "500"
