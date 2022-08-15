# Azure-IoT-Hub-Device-Python-Example
Both Azure IoT Hub Device example and Azure IoT Device Provisioning Service enrollment example, written in Python. It supports both D2C and C2D communication.

## Blog post
Check out the [blog post](https://sandervandevelde.wordpress.com/2022/01/24/azure-iot-deviceclient-sdk-python-demonstration-the-basics/) behind this sample code for more background information.

## Two examples

Both examples are exposing the same logic.

### IoT Hub - Device connection string

This code expects an Environment variable named 'IOTHUB_DEVICE_CONNECTION_STRING' to be present. Otherwise the app will fail to authenticate. See the blog post for instructions.

### DPS - individual enrollment, symmetric key

This code expects Environment variables named "PROVISIONING_HOST", "PROVISIONING_IDSCOPE", "PROVISIONING_REGISTRATION_ID", and "PROVISIONING_SYMMETRIC_KEY".

## Usage

### Device Twin call

On startup, the device will ask for any Device twin information. It will receive both the desired and reported properties.

### Direct Method event handler

You can send an interval (in seconds) to 'SetTelemetryInterval'. No JSON format neede, junst ths integer.

### Cloud message event handler

Just send some string to the device. It will show the received text in the console output.

### Device Twin desired properties change event handler

Send a Device twin desired property change. It will be shown in the console output.

The device will respond with a reported property update.


## Resources
This code is based on thiese resources:

* https://github.com/Azure-Samples/azure-iot-samples-python/tree/master/iot-hub/Quickstarts/simulated-device-2
* https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/sync-samples/receive_message.py
* https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-python-twin-getstarted#create-the-device-app

Check out the details there for more indept information.

