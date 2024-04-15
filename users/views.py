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


class Logout(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
            return Response({
                'type':"successful",
                'detail':"تم تسجيل الخروج بنجاح"
                })
    

class UserRegisterView(generics.CreateAPIView):
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


class EmailRequest(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email',None)
        if not email:
            raise ValidationError({'error':'email field is missing .'})
        try:
            user = User.objects.get(email=email)
            token = Token.objects.get(user=user)
        except User.DoesNotExist:
            raise ValidationError({
                'type':'error',
                'detail':'برجاء التأكد من الايميل , لايوجد حساب مسجل بهاذا الايميل'
                })
        # send_email.delay(user_email=user.email,user_otp=user.otp)
        message = {
            'type':"successful",
            'detail':"تم ارسال كود التأكيد بنجاح",
            'token':token.key,
        }
        return Response(message,status=status.HTTP_200_OK)


class ResetPassword(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        otp = request.data.get('otp',None)
        new_password = request.data.get('new_password',None)
        if not otp or not new_password:
            raise ValidationError({'error':'otp/new_password is missing'})
        if otp != user.otp:
            raise ValidationError({
                'type':"error",
                'detail':"لقد قمت بأدخال كود تفعيل خاطئ"
                })
        user.set_password(new_password)
        user.save()
        message = {
            'type':"successful",
            'detail':"تـم تغير كلمة المرور بنجاح"
        }
        return Response(message,status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView,generics.RetrieveAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    def get_object(self):
        return self.request.user

class SMSAuthentication(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        email:str = request.query_params.get('email')
        if not email or '@' not in email:
            raise ValidationError({'type':'error',
                'detail':'the email is not found or not valid .'
                })
        otp = generate_otp_code()
        # send_email.delay(email,otp)
        return Response(
            data= {
                'type':"successful",
                'otp':otp,
            },
            status=status.HTTP_200_OK            
        )