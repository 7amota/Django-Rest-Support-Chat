from .models import User, Message, Ticket
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    class Meta:
        model = Message
        fields = ("id",'message','sender',"sender_email",'ticket')

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ['id','user']
    def create(self, validated_data):
        obj, created = Ticket.objects.get_or_create(user=validated_data['user'])
        return obj

class TicketRetriveSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True,source='message_set')
    class Meta:
        model = Ticket
        fields = ['id','user','messages']
 