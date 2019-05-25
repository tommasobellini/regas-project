import channels
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json

from sensors.models import Sensor, SensorLine


class StoreConsumer(AsyncWebsocketConsumer):
    group_name = 'store'

    async def connect(self):
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = text_data
        await self.store_data(text_data_json)

    @database_sync_to_async
    def store_data(self, text_data):
        Sensor.objects.create(**text_data)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


class CoreConsumer(AsyncWebsocketConsumer):
    group_name = 'core'

    async def connect(self):
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data['data']

        await self.store_data(data)

        await self.channel_layer.group_send(
            'core',
            {
                'type': 'send_data_to_client',
                'data': data
            }
        )


    @database_sync_to_async
    def store_data(self, text_data):
        sensor_data = {}
        sensors_info = text_data['sensor_info'].split(',')
        sensor_data['name'] = sensors_info[0].split('=')[1]
        sensor_data['version'] = sensors_info[1].split('=')[1]
        sensor_data['max_value'] = int(sensors_info[2].split('=')[1].split('.')[0], base=10)
        sensor_data['min_value'] = int(sensors_info[3].split('=')[1].split('.')[0], base=10)

        sensor = Sensor.objects.get_or_create(location=text_data['location'],**sensor_data)[0]
        if sensor:
            data_dict = {}
            data_dict['humidity'] = text_data['humidity'].split('%')[0]
            data_dict['temperature'] = text_data['temperature'].split('°C')[0]
            data_dict['sensor'] = sensor
            SensorLine.objects.create(**data_dict)
            text_data['sensor'] = sensor.pk


    async def send_data_to_client(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        return self.disconnect(code)


class SensorConsumer(AsyncWebsocketConsumer):
    group_name = 'sensor'

    async def connect(self):
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        return self.disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data['data']
        await self.channel_layer.group_send(
            'sensor',
            {
                'type': 'send_data_to_client',
                'data': data
            }
        )

    async def send_data_to_client(self, event):
        data = event['data']
        new_dict = {}
        new_dict['temp_graph'] = data['temp_graph']
        await self.send(text_data=json.dumps(new_dict))
