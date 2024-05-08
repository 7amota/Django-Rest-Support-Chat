from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import UserSerializer, UserUpdateSerializer
from .utlis import generate_otp_code

from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, get_user_model
User= get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        if not email or not password:
            raise ValidationError({'error':"The email or password is not found ."})
        user = authenticate(email=email,password=password)

        if not user:
            raise ValidationError({
                'type':"error",
                'detail':"الايميل او الباسورد غير صحيح , برجاء التأكد منهم"
                })
        refresh = RefreshToken.for_user(user)
        userData = UserSerializer(instance=user,context={'request':request})
        message = {
            'type':"successful",
            'detail':"تم تسجيل الدخول بنجاح ",
            'data':userData.data,
            'token':{
                'access':str(refresh.access_token),
                'refresh':str(refresh)
            }
        }
        return Response(message,status.HTTP_200_OK)


    

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            token = RefreshToken.for_user(user=serializer.instance)
            success_message = {
                'type':"successful",
                'detail':'تم انشاء الحساب بنجاح',
                'data':serializer.data,
                'token':{
                    'access':str(token.access_token),
                    'refresh':str(token.access_token),
                }
            }

            return Response(success_message,status=status.HTTP_200_OK)

class UserUpdateView(generics.UpdateAPIView,generics.RetrieveAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    def get_object(self):
        return self.request.user

