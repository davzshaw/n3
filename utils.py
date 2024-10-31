import base64
import os
import requests

path = "storage/"

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
        return "200"
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
                
def readFiles(filename = "datetime.txt"):
    try:
        with open(path+filename, "r") as file:
            return file.read()
        return "200"
    except:
        return "500"

def writeFiles(content, filenameOutput):
    try:
        with open(path+filenameOutput, "w") as file:
            file.write(content)
        return "200"
    except:
        return "500"
        

