# detector.py
import time
import random
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"  
TOPIC_PING = "ping"
TOPIC_ACK = "ack"
SUSPICION_THRESHOLD = 3  

def on_message(client, userdata, message):
    if message.topic == TOPIC_ACK:
        print("Detector: Received ACK")
        client.ack_received = True  
def detector():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER)
    client.loop_start()
    client.subscribe(TOPIC_ACK)

    suspicion_count = 0  

    while True:
        client.ack_received = False  
        print("Detector: Sending Ping")
        client.publish(TOPIC_PING, "Ping")
        
        for _ in range(20):  
            time.sleep(0.1)
            if client.ack_received:
                suspicion_count = 0  
                break
        
        if not client.ack_received:
            suspicion_count += 1  
            print(f"Detector: No ACK received, suspicion count: {suspicion_count}")
            if suspicion_count >= SUSPICION_THRESHOLD:
                print("Detector: Assumed crash after multiple missed pings!")
                break  
            
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    detector()