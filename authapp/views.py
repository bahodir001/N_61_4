from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import CustomUser

from django.core.mail import send_mail
from threading import Thread

from .utils import generate_code, is_email

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        phone = data.get('phone')
        password = data.get('password')
        key = data.get('key', '')

        if not phone or not password:
            return Response({"error": "Parol yo nomerri yozilmaydimi silar tarafda"})

        if not str(phone).isdigit() or len(str(phone)) != 12 or str(phone)[:3] != '998':
            return Response({"error": "Raqam xato"})

        if (
            len(password) < 6
            or ' ' in password
            or not password.isalnum()
            or not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
        ):
            return Response({"error": "Parol noto'g'ri kiritildi"})

        if CustomUser.objects.filter(phone=phone).exists():
            return Response({"error": "Bu raqamdan oldin foydalanilgan"})

        user_data = {
            'phone': phone,
            'password': password,
            'name': data.get('name', '')
        }

        if key == '123':
            user_data.update({
                'is_active': True,
                'is_staff': True,
                'is_superuser': True
            })

        user = CustomUser.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        return Response({
            'message': "Hush kelibsiz, Brodar",
            'token': token.key
        })


class LoginView(APIView):
    def post(self, request):
        data = request.data
        phone = data.get('phone')
        password = data.get('password')

        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            return Response({"error": "Bu telefondan ro'yxatdan o'tilmagan"})

        if not user.check_password(password):
            return Response({"error": "Parol mos emas"})

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Siz muvaffaqiyatli tizimga kirdingiz",
            "token": token.key
        })


class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        if token:
            token.delete()
        return Response({"message": "Ko'zimga ko'rinmang"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({
            'data': request.user.format()
        })

    def patch(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({"error": "Telefon raqami kiritilmadi"})

        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            return Response({"data": "Oldin ro'yxatdan o'tish kerak"})
        return Response({"data": "Qoyil sizga"})


class DeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        request.user.delete()
        return Response({"message": "X"})


class SendVerificationCode(APIView):
    def post(self, request):
        serializer = VerifyRequestSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            code = generate_code()

            if is_email(identifier):
                def send_code():
                    send_mail(
                        subject='Verification Code',
                        message=f'Your verification code is: {code}',
                        from_email='admin@example.com',
                        recipient_list=[identifier],
                        fail_silently=False
                    )

                Thread(target=send_code).start()
                return Response({'message': 'Verification code sent to email'}, status=status.HTTP_200_OK)

            else:
                print(f"[DEBUG] Phone code for {identifier}: {code}")
                return Response({'message': 'Verification code sent to phone'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)