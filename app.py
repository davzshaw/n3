from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime
from soundmanager import isCrying, processAudioFiles
from utils import *

app = Flask(__name__)

# Controllers

@app.route('/get/datetime', methods=['GET'])
def getDatetime():
    try:
        datetime_data = readFiles("datetime.txt")
        return jsonify({"response": datetime_data}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to get datetime - {str(e)}"}), 500

@app.route('/get/temperature', methods=['GET'])
def getTemperature():
    try:
        temperature = readFiles("temp.txt")
        return jsonify({"response": temperature}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to get temperature - {str(e)}"}), 500

@app.route('/get/cry', methods=['GET'])
def getCry():
    try:
        sound = readFiles("cry.txt")
        return jsonify({"response": sound}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to get sound - {str(e)}"}), 500
    
@app.route('/get/setting', methods=['GET'])
def getSetting():
    try:
        settings = readFiles("setting.txt")
        return jsonify({"response": settings}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to get settings - {str(e)}"}), 500
    
@app.route('/insert/datetime', methods=['POST'])
def insertDatetime():
    try:
        if not request.json:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writeFiles(datetime_string, "datetime.txt")
        return jsonify({"response": "Datetime inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to insert datetime - {str(e)}"}), 500

@app.route('/insert/temperature', methods=['POST'])
def insertTemperature():
    try:
        if not request.json or 'data' not in request.json:
            return jsonify({"error": "Data not provided"}), 400
        
        data = request.json.get('data')
        writeFiles(data, "temp.txt")
        return jsonify({"response": "Temperature inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to insert temperature - {str(e)}"}), 500

@app.route('/insert/cry', methods=['POST'])
def insertCry():
    try:
        if not request.json or 'data' not in request.json:
            return jsonify({"error": "Data not provided"}), 400
        
        data = request.json.get('data')
        writeFiles(data, "cry.txt")
        return jsonify({"response": "Cry inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to insert cry - {str(e)}"}), 500

@app.route('/insert/setting', methods=['POST'])
def insertSetting():
    try:
        if not request.json or 'data' not in request.json:
            return jsonify({"error": "Data not provided"}), 400
        
        data = request.json.get('data')
        writeFiles(data, "setting.txt")
        return jsonify({"response": "Setting inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to insert setting - {str(e)}"}), 500

@app.route('/clear', methods=['POST'])
def clear():
    try:
        deleteFiles()
        return jsonify({"response": "Files deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to delete files - {str(e)}"}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not request.json or 'data' not in request.json:
            return jsonify({"error": "Data not provided"}), 400
        
        data = request.json.get('data')
        sounds = [data]
        rms, frequency, pitch, duration = processAudioFiles(sounds)
        cry = isCrying(rms, frequency, pitch, duration)
        
        cry_response = "yes" if cry else "no"
        writeFiles(cry_response, "cry.txt")
        
        to_return = {"response": cry}
        return jsonify(to_return), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to process prediction - {str(e)}"}), 500

@app.route('/send', methods=['POST'])
def sendAlert():
    try:
        cry = readFiles("cry.txt")
        temp = readFiles("temp.txt")
        crybool = cry == "yes"
        
        intervalsA = (-999, 15)
        intervalsB = (28, 999)
        
        if -999 <= int(temp) <= 15 or 28 <= int(temp) <= 999:
            sendEmail(crybool, temp)
        return jsonify({"response": "Mail sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error trying to send alert - {str(e)}"}), 500

# Pages
@app.route('/')
def index():
    try:
        datetime_data = readFiles("datetime.txt")
        temp_data = readFiles("temp.txt")
        cry_data = readFiles("cry.txt")
        
        if datetime_data.strip() == "deleted":
            datetime_data = "1/1/1 00:00:00"
        
        if temp_data.strip() == "deleted °C" or (not str(temp_data.strip())[0].isdigit()):
            temp_data = "0"
        
        if cry_data.strip() == "deleted":
            cry_data = "unknown"

        return render_template('index.html', datetime=datetime_data, temperature=temp_data, cry=cry_data)
    except Exception as e:
        return f"Error loading page: {str(e)}"

@app.route('/setting')
def setting():
    return render_template('setting.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
