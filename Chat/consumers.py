# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Chat.models import ChatRoom,Message
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # 🔥 Broadcast JOIN event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'user': user.username
            }
        )

    async def disconnect(self, close_code):
        user = self.scope["user"]

        # 🔥 Broadcast LEAVE event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user': user.username
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        
    async def receive(self, text_data): 
        data = json.loads(text_data) 
        message = data['message'] 
        user = self.scope["user"] 
        # Save message 
        await self.save_message(user, message) 
        await self.channel_layer.group_send( self.room_group_name, 
        { 'type': 'chat_message', 'message': message, 'user': user.username } ) 
        
    async def chat_message(self, event): await self.send(text_data=json.dumps(event)) 
    async def save_message(self, user, message):
        from asgiref.sync import sync_to_async

        room, created = await sync_to_async(ChatRoom.objects.get_or_create)(
            name=self.room_name
        )

        await sync_to_async(Message.objects.create)(
            room=room,
            sender=user,
            content=message
        )
    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'join',
            'message': f"{event['user']} joined the room"
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'message': f"{event['user']} left the room"
        }))