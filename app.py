from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'halloween/buttons')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'username')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'password')

def send_mqtt_message(command):
    """Send MQTT message"""
    try:
        client = mqtt.Client()
        
        # Set username and password if provided
        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        client.connect(MQTT_BROKER, MQTT_PORT, 61)
        client.publish(MQTT_TOPIC, command)
        client.disconnect()
        return True
    except Exception as e:
        print(f"Error sending MQTT message: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button1', methods=['POST'])
def button1():
    success = send_mqtt_message('COMMAND_1')
    return jsonify({'success': success, 'command': 'COMMAND_1'})

@app.route('/button2', methods=['POST'])
def button2():
    success = send_mqtt_message('COMMAND_2')
    return jsonify({'success': success, 'command': 'COMMAND_2'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

