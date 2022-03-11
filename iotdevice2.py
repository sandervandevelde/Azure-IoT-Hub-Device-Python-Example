# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import os
import logging
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from pyparsing import empty

logging.basicConfig(level=logging.INFO)

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'
MSG_LOG = '{{"Name": {name},"Payload": {payload}}}'

INTERVAL = 2

def create_client():
    # Create an IoT Hub client

    model_id = "dtmi:com:example:NonExistingController;1"

    client = IoTHubDeviceClient.create_from_connection_string(
                CONNECTION_STRING,
                product_info=model_id,
                websockets=True)  # used for communication over websockets (port 443)

    # *** Direct Method ***
    #
    # Define a method request handler
    def method_request_handler(method_request):
        
        print(MSG_LOG.format(name=method_request.name, payload=method_request.payload))

        if method_request.name == "SetTelemetryInterval":
            try:
                global INTERVAL
                INTERVAL = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}, interval updated".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse.create_from_method_request(method_request, response_status, response_payload)
        client.send_method_response(method_response)

    # *** Cloud message ***
    #
    # define behavior for receiving a message
    def message_received_handler(message):
        print("the data in the message received was ")
        print(message.data)
        print("custom properties are")
        print(message.custom_properties)

    # *** Device Twin ***
    #
    # define behavior for receiving a twin patch
    # NOTE: this could be a function or a coroutine
    def twin_patch_handler(patch):
        print("the data in the desired properties patch was: {}".format(patch))
        # Update reported properties with cellular information
        print ( "Sending data as reported property..." )
        reported_patch = {"reportedValue": 42}
        client.patch_twin_reported_properties(reported_patch)
        print ( "Reported properties updated" )

    try:
        # Attach the direct method request handler
        client.on_method_request_received = method_request_handler

        # Attach the cloud message request handler
        client.on_message_received = message_received_handler

        # Attach the Device Twin Desired properties change request handler
        client.on_twin_desired_properties_patch_received = twin_patch_handler

        client.connect()

        twin = client.get_twin()
        print ( "Twin at startup is" )
        print ( twin )
    except:
        # Clean up in the event of failure
        client.shutdown()
        raise

    return client


def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

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


def main():
    print ("IoT Hub Quickstart #2 - Simulated device")
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
