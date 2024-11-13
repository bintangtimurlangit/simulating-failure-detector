# crash_process.py
import time
import random
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"  
TOPIC_PING = "ping"
TOPIC_ACK = "ack"

def on_message(client, userdata, message):
    if message.topic == TOPIC_PING:
        print("Crash Process: Received Ping")
        crash_chance = random.random()
        if crash_chance < 0.4:  
            print("Crash Process: Crashing!")
            return  
        elif crash_chance < 0.2:  
            print("Crash Process: Temporary failure, not responding.")
            return 
        
        print("Crash Process: Sending ACK")
        client.publish(TOPIC_ACK, "ACK")

def crash_process():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER)
    client.loop_start()
    client.subscribe(TOPIC_PING)

    while True:
        time.sleep(1)  

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    crash_process()