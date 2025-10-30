# MQTT Button Controller

A simple web application for Raspberry Pi that provides two buttons to send different MQTT commands.

## Project Structure

```
halloween-proj/
├── Dockerfile
├── compose.yml
├── .dockerignore
├── .gitignore
├── .env (you create this)
├── requirements.txt
├── app.py
├── templates/
│   └── index.html
└── mosquitto/
    └── config/
        ├── pwfile (you create this)
        └── mosquitto.conf
```

## Quick Start

### 1. Prerequisites

Install Docker on your Raspberry Pi:

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Log out and back in for group changes to take effect.

### 2. Configure

**Fix file ownership issue:**

Find your user ID and group ID:

```bash

id -u  # Your user ID
id -g  # Your group ID
```

Add these to your `.env` file to prevent Mosquitto from changing file ownership:

```bash
MOSQUITTO_UID=1000  # Replace with your user ID
MOSQUITTO_GID=1000  # Replace with your group ID
```

The `mosquitto.conf` file is already provided. A `pwfile` is used for password management of the MQTT Broker. Run the following to set it up:

```bash
docker run -it --rm -v $(pwd)/mosquitto/config:/mosquitto/config mqtt mosquitto_passwd -c /mosquitto/config/pwfile your_username
```

Create a `.env` file in the project directory:

```bash
cp .env.example .env
nano .env
```

Update the values in `.env`:

```bash
MOSQUITTO_UID=1000  # Your user ID (from 'id -u')
MOSQUITTO_GID=1000  # Your group ID (from 'id -g')

MQTT_BROKER=mqtt
MQTT_PORT=1883
MQTT_TOPIC=home/buttons

MQTT_USERNAME=your_username  # If using auth
MQTT_PASSWORD=your_password  # If using auth
```

**Important:**

- Use `mqtt` as the broker name for container-to-container communication
- Set MOSQUITTO_UID and MOSQUITTO_GID to your user's IDs to prevent ownership issues
- Never commit your `.env` file to version control!

### 3. Deploy

Build and start the container:

```bash

docker-compose up -d
```

### 4. Access

Open your browser and navigate to:

```
http://your-raspberry-pi-ip:5000
```

## Docker Commands

### Start the application

```bash

docker-compose up -d
```

### Stop the application

```bash
docker-compose down
```

### View logs

```bash
docker-compose logs -f
```

### Rebuild after changes

```bash
docker-compose up -d --build
```

### Restart the application

```bash
docker-compose restart
```

## Customization

### Change MQTT Commands

Edit `app.py` and modify the commands in the route handlers:

```python

@app.route('/button1', methods=['POST'])
def button1():
    success = send_mqtt_message('YOUR_COMMAND_1')
    return jsonify({'success': success, 'command': 'YOUR_COMMAND_1'})
```

### Change Button Labels

Edit `templates/index.html` and update the button text:

```html
<button id="btn1" onclick="sendCommand(1)">Your Label 1</button>
<button id="btn2" onclick="sendCommand(2)">Your Label 2</button>
```

After making changes, rebuild:

```bash
docker-compose up -d --build
```

## Troubleshooting

### Container won't start

Check logs:

```bash
docker-compose logs
```

### Can't connect to MQTT broker

- Verify MQTT broker IP is correct
- Ensure MQTT broker is running
- Check firewall rules
- Verify network connectivity: `ping your-mqtt-broker-ip`

### Can't access web interface

- Verify the container is running: `docker ps`
- Check if port 5000 is available: `sudo netstat -tulpn | grep 5000`
- Try accessing from the Pi itself: `http://localhost:5000`

## Auto-start on Boot

The container is configured with `restart: unless-stopped`, so it will automatically start when your Raspberry Pi boots up.

## Updating

To update the application:

1. Make your changes to the files
2. Rebuild and restart:

```bash
docker-compose down
docker-compose up -d --build
```

## Security Notes

- Consider using MQTT with TLS/SSL for production
- Don't expose port 5000 to the internet without authentication
- Use strong MQTT credentials
- Consider adding basic auth to the web interface for added security
