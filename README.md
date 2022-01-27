# Azure-IoT-Hub-Device-Python-Example
Azure IoT Hub Device example, written in Python. It supports both D2C and C2D communication

## Blog post
Check out the [blog post](https://sandervandevelde.wordpress.com/2022/01/24/azure-iot-deviceclient-sdk-python-demonstration-the-basics/) behind this sample code for more background information.

## Device connection string

This code expects an Environment variable named 'IOTHUB_DEVICE_CONNECTION_STRING' to be present. Otherwise the app will fail to authenticate. See the blog post for instructions.

## Resources
This code is based on thiese resources:

* https://github.com/Azure-Samples/azure-iot-samples-python/tree/master/iot-hub/Quickstarts/simulated-device-2
* https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/sync-samples/receive_message.py
* https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-python-twin-getstarted#create-the-device-app

Check out the details there for more indept information.

