from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import MyTrips
from .serializers import MyTripsSerializer
from asgiref.sync import async_to_sync, sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']
        date_added = data['date_added']
        trip = data['trip']
        requestData = data['requestData']

        await self.add_message(trip, requestData)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user,
                'date_added': date_added,
            }
        )
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        date_added = event['date_added']
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'date_added': date_added,
        }))

    async def add_message(self, trip, requestData):
        trip = await sync_to_async(MyTrips.objects.get)(id=trip.get('id'))

        serializer = await sync_to_async(MyTripsSerializer)(instance=trip, data=requestData)
        if (await sync_to_async(serializer.is_valid)()):
            await sync_to_async(serializer.save)()
        return 'Successfully updated trip!'