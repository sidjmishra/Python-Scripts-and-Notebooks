# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import signal
import threading
import json
from azure.iot.device.aio import IoTHubModuleClient

from azure.iot.device import Message
from simulator import pdm_simulator


# Event indicating client stop
stop_event = threading.Event()

client = IoTHubModuleClient.create_from_edge_environment()
async def create_client():

    # Define function for handling received messages
    # async def receive_message_handler(message):
        # Messages sent to other inputs, or to the default, will be discarded

    try:
        # Set handler on the client
        print("Try Block")
        # print("The data message received: ")
        # msg = pdm_simulator()
        # print("forwarding mesage to output1")
        # await client.send_message_to_output(Message(msg), "pdmOutput")
        # receive_message_handler(Message(msg))
        # client.on_message_received = receive_message_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    print("Outside Loop")
    print("The data message received: ")
    msg = pdm_simulator()
    print("forwarding mesage to output1")
    await client.send_message_to_output(json.dumps(msg), "pdmOutput")
    while True:
        await asyncio.sleep(10)
        print("Inside Loop")

def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    # client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
