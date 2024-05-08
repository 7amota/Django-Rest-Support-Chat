from rest_framework import generics,status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import TicketSerializer,TicketRetriveSerializer
from .models import Ticket


class TicketsViewset(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TicketSerializer
    lookup_field = 'id'
    http_method_names = ['get','delete','post']

    def get_serializer_class(self):
        if self.action in ['list']:
            return TicketSerializer
        if self.action in ['retrieve']:
            return TicketRetriveSerializer
        return TicketSerializer
    
    def get_permissions(self):
        if self.action in ['list','create']:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]
    
    def filter_queryset(self, queryset):
        user = self.request.user
        if not user.is_staff:
            return self.queryset.filter(user=user)
        else:
            return super().filter_queryset(queryset)
        
    @action(detail=True,methods=['POST'])
    def claim_ticket(self,request,id):
        user = request.user
        try:
            ticket = Ticket.objects.get(id=id)
        except:
            raise ValidationError({'detail':"The ticket object is not valid"})
        admins_on_ticket = ticket.admins
        if user in admins_on_ticket.all():
            raise ValidationError({'detail':"you r already in this ticket"})
        admins_on_ticket.add(user)
        return Response({'detail':"The admin added successfuly to the ticket"})
    @action(detail=True,methods=['POST'])
    def get_ticket(self,request,id):
        ticket = Ticket.objects.get(id=id)
        return Response({'detail':ticket.pk})