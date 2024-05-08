from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "username" ,"password","phoneNumber", "image" , "location" , "dateBirth",'gender']
        
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError({"email":"Email is already used, try another one"})
        return attrs
    def create(self, validated_data):
      password = validated_data.pop("password")
      user = super().create(validated_data)
      user.set_password(password)
      user.save()
      return user
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80, required=False)
    username = serializers.CharField(max_length=45,required=False)
    class Meta:
        model = User
        fields = ['email', 'image', 'username', 'phoneNumber', 'dateBirth', 'location','gender']
    def validate(self, attrs):
        email = attrs.get('email',None)
        if email:
            if User.objects.filter(email=attrs['email']).exists():
                raise ValidationError({"email":"الايميل مستخدم سابقاً , حاول بأيميل اخر"})
        return attrs
