# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from asyncio.windows_events import NULL
import random
from azure.iot.device import ProvisioningDeviceClient
import os
import time
from azure.iot.device import IoTHubDeviceClient, Message
import uuid

provisioning_host = os.getenv("PROVISIONING_HOST")
id_scope = os.getenv("PROVISIONING_IDSCOPE")
registration_id = os.getenv("PROVISIONING_REGISTRATION_ID")
symmetric_key = os.getenv("PROVISIONING_SYMMETRIC_KEY")

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'
MSG_LOG = '{{"Name": {name},"Payload": {payload}}}'

INTERVAL = 2

def create_client():

    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )

    registration_result = provisioning_device_client.register()
    # The result can be directly printed to view the important details.
    print(registration_result)

    # Individual attributes can be seen as well
    print("The status was :-")
    print(registration_result.status)
    print("The etag is :-")
    print(registration_result.registration_state.etag)

    if registration_result.status == "assigned":
        print("Will send telemetry from the provisioned device")
        # Create device client from the above result
        client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
        )

        return client
    else:
        print("Can not send telemetry from the provisioned device")
        return NULL


def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    if client != NULL:

        # Connect the client.
        client.connect()

        while True:
            # *** Sending a message ***
            #
            # Build the message with simulated telemetry values.
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
                message.custom_properties["temperatureAlert"] = "true"
            else:
                message.custom_properties["temperatureAlert"] = "false"


            # Send the message.
            print("Sending message: {}".format(message))
            client.send_message(message)

            print("Message sent")
            time.sleep(INTERVAL)

    else:
        print("client not created")
    
def main():
    print ("IoT Hub - DPS Quickstart - Simulated device via DPS individual enrollment - symmetric key")
    print ("Press Ctrl-C to exit")

    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = create_client()

    # Send telemetry
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        print("Shutting down IoTHubClient")
        client.shutdown()


if __name__ == '__main__':
    main()