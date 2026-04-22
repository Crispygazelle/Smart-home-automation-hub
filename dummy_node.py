import paho.mqtt.client as mqtt

# Configuration
BROKER = "localhost" # It looks for the Mosquitto broker on this Pi
PORT = 1883
TOPIC = "home/living_room/light"

# What to do when it connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[*] Node connected to MQTT Broker successfully!")
        client.subscribe(TOPIC)
        print(f"[*] Listening for commands on topic: {TOPIC}")
    else:
        print(f"[!] Failed to connect. Code: {rc}")

# What to do when it receives a message
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"\n[RECEIVED] Topic: {msg.topic} | Command: {command}")
    
    if command == "ON":
        print("   -> ? CLICK! The physical relay turns ON.")
        # Real hardware GPIO code would trigger here
    elif command == "OFF":
        print("   -> ? CLICK! The physical relay turns OFF.")
        # Real hardware GPIO code would trigger here
    else:
        print("   -> [!] Unknown command.")

# Setup and run the client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"LivingRoomLight_Node")
client.on_connect = on_connect
client.on_message = on_message

print("Powering up simulated hardware node...")
client.connect(BROKER, PORT, 60)

# Keep the script running to listen for messages
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nNode unplugged. Shutting down.")
    client.disconnect()
