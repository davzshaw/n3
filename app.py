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
        datetime = readFiles("datetime.txt")
        return jsonify({"response": datetime}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to get datetime - {e}"}), 500

@app.route('/get/temperature', methods=['GET'])
def getTemperature():
    try:
        temperature = readFiles("temp.txt")
        return jsonify({"response": temperature}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to get temperature - {e}"}), 500

@app.route('/get/cry', methods=['GET'])
def getCry():
    try:
        sound = readFiles("cry.txt")
        return jsonify({"response": sound}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to get sound - {e}"}), 500
    
@app.route('/get/setting', methods=['GET'])
def getSetting():
    try:
        settings = readFiles("setting.txt")
        return jsonify({"response": settings}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to get settings - {e}"}), 500
    
@app.route('/insert/datetime', methods=['POST'])
def insertDatetime():
    try:
        data = request.json.get('data')
        datetimeString = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writeFiles(datetimeString, "datetime.txt")
        return jsonify({"response": "Datetime inserted successfully"}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to insert datetime - {e}"}), 500

@app.route('/insert/temperature', methods=['POST'])
def insertTemperature():
    try:
        data = request.json.get('data')
        writeFiles(data, "temp.txt")
        return jsonify({"response": "Temperature inserted successfully"}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to get temperature - {e}"}), 500


@app.route('/insert/cry', methods=['POST'])
def insertCry():
    try:
        data = request.json.get('data')
        writeFiles(data, "cry.txt")
        return jsonify({"response": "Cry inserted successfully"}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to insert cry - {e}"}), 500

@app.route('/insert/setting', methods=['POST'])
def insertSetting():
    try:
        data = request.json.get('data')
        writeFiles(data, "setting.txt")
        return jsonify({"response": "Setting inserted successfully"}), 200
    except Exception as e:
        return e
    
@app.route('/clear', methods=['POST'])
def clear():
    try:
        deleteFiles()
        return jsonify({"response": "Files deleted successfully"}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to delete files - {e}"}), 500
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get('data')
        sounds = [data]
        rms, frequency, pitch, duration = processAudioFiles(sounds)
        cry = isCrying(rms, frequency, pitch, duration)
        if cry:
            writeFiles("yes", "cry.txt")
        else:
            writeFiles("no", "cry.txt")
        toReturn = {"response": cry}
        return jsonify(toReturn), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to delete files - {e}"}), 500


# Pages
@app.route('/')
def index():
    try:
        datetime_data = readFiles("datetime.txt")
        temp_data = readFiles("temp.txt")
        cry_data = readFiles("cry.txt")
        
        if datetime_data.strip() == "deleted":
            datetime_data = "1/1/1 00:00:00"
            
        if temp_data.strip() == "deleted °C":
            temp_data = "0"
            
        if cry_data.strip() == "deleted":
            cry_data = "unknow"

        return render_template('index.html', datetime=datetime_data, temperature=temp_data, cry=cry_data)
    except Exception as e:
        return f"Error al cargar la página: {e}"

@app.route('/setting')
def setting():
    return render_template('setting.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)