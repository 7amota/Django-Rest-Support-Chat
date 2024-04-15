from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import InvalidChannelLayerError
from asgiref.sync import async_to_sync
from rest_framework.exceptions import ValidationError

from ..models import Ticket, Message
from ..serializers import MessageSerializer

import json



class ChatConsumer (WebsocketConsumer) :

    def connect(self):
        self.user = self.scope['user']
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.group_name = f"chat_{self.ticket_id}"
        self.ticket = self.get_ticket()
        print(self.ticket)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type":"send_msg",
                "msgs":self.get_messages(),
            }
        )
        self.accept()
    
    def receive(self, text_data):
        message = text_data
        msg = self.save_msg(msg=message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':"send_msg",
                'msgs':msg
            }
        )

    def get_ticket(self):
        try:
            if self.user.is_staff:
                    ticket = Ticket.objects.get(id=self.ticket_id)
                    if not self.user in ticket.admins.all():
                        self.disconnect(code=400)
            else:
                    ticket = Ticket.objects.get(id=self.ticket_id,user=self.user)
            return ticket
        except:
             self.disconnect(code=400)

    def save_msg(self,msg):
        create_msg = Message.objects.create(sender=self.user,message=msg,ticket=self.ticket)   
        return MessageSerializer(create_msg).data
    
    def send_msg (self, data) : 
        json_msgs = json.dumps(data['msgs'])
        self.send(text_data=json_msgs)
    
    def get_messages(self):
        messages = Message.objects.filter(ticket=self.ticket)
        return MessageSerializer(many=True,instance=messages).data
    
    def disconnect(self, code):
         async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
         self.close()