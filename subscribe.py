import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/living_room_temperature_my_house"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    ''' Authentication function'''
    
    def on_connect(client, userdata, flags, rc):
        ''' Callback function for connecting the broker. This function is
            called after the client has successfully connected.'''
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect to MQTT Broker, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    ''' Subscribe function. '''
    
    def on_message(client, userdata, msg):
        ''' Callback for when a message has been received '''
        # Parse only the temperature from the received message.
        discard, seperator, temperature = msg.payload.decode().partition(' ')

        # Make the fan state off by default.
        state = "Off"

        # The fan is only on if the temperature is greater than 70 degrees.
        if int(temperature) > 70:
            state = "On"

        # Inform the end-user of the temperature and fan state.
        print(f"Current Temperature is {temperature} degrees - fan {state}")

    client.subscribe(topic)

    # Wire the on_message event to the callback function so that the
    # callback function gets called when a message is received.
    client.on_message = on_message

def run():
    ''' run function. Authenticate, subscribe to the publisher, and loop. '''
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
