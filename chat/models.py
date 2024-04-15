from django.db import models

from users.models import User

class Ticket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User,related_name='admins',blank=True)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE) 
    message = models.CharField(max_length=550)
