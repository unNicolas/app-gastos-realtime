import json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.identity.aio import DefaultAzureCredential
import streamlit as st
from azure.eventhub import TransportType
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

EVENT_HUB_CONNECTION_STR = os.getenv("eventhubConSt")
EVENT_HUB_NAME = os.getenv("eventhubName")


async def run(event_data):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()
        print(f"Event Data: {event_data}")
        json_data = json.dumps(event_data)

        # Codificar la cadena JSON en UTF-8
        encoded_data = json_data.encode('utf-8') 

        # Add events to the batch.
        event_data_batch.add(EventData(encoded_data))


        # Send the batch of events to the event hub.
        try:
            await producer.send_batch(event_data_batch)
            st.success('¡Gasto registrado exitosamente!')
        except Exception as e:
            st.error(f"Error al enviar el evento a Event Hubs: {e}")
