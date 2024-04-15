from django.contrib import admin
from .models import User
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email','username','location','gender','phoneNumber')
    list_filter = ['email','username','phoneNumber','gender']
admin.site.register(User,UserModelAdmin)