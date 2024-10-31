from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime
from utils import *

app = Flask(__name__)

# Controllers

mainUrl = "https://n2.onrender.com/api"

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
        sound = readFiles("sound.txt")
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
        datetimeString = datetime.fromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S')
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
        writeFiles(data, "sound.txt")
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
        return jsonify({f"error": "Error trying to insert setting - {e}"}), 500
    
@app.route('/clear', methods=['POST'])
def clear():
    try:
        deleteFiles()
        return jsonify({"response": "Files deleted successfully"}), 200
    except Exception as e:
        return jsonify({f"error": "Error trying to delete files - {e}"}), 500


# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)