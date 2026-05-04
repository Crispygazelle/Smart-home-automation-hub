import sqlite3
from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT Setup
BROKER = "localhost"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Flask_Backend")
client.connect(BROKER, 1883, 60)
client.loop_start() # Runs MQTT network traffic in a background thread

def get_db_connection():
    conn = sqlite3.connect('smarthome.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()
    return render_template('index.html', devices=devices)

@app.route('/api/toggle', methods=['POST'])
def toggle():
    data = request.get_json()
    device_id = data['device_id']
    topic = data['topic']
    command = data['command']

    # 1. Publish to the physical hardware via MQTT
    client.publish(topic, command)

    # 2. Update the persistent state in SQLite
    conn = get_db_connection()
    conn.execute('UPDATE devices SET current_state = ? WHERE device_id = ?', (command, device_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "state": command})

if __name__ == '__main__':
    # Listen on all network interfaces so you can access it from your Mac
    app.run(host='0.0.0.0', port=5000, debug=True)
