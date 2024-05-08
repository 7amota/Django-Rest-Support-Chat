from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


from rest_framework.authtoken.models import Token


User = get_user_model()
@receiver(post_save,sender=User)
def token_creation_user(instance,created=False,*args, **kwargs):
    if created:
        Token.objects.create(user=instance)