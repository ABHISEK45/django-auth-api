from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import EmailOTP
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    UserSerializer
)

from .utils import generate_otp


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
            request_body=RegisterSerializer,
            operation_description="Register a new user and send OTP to email"
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "User already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = email.split("@")[0]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False
            )

            otp = generate_otp()

            EmailOTP.objects.create(
                user=user,
                otp=otp
            )

            send_mail(
                subject="Your OTP Verification Code",
                message=f"Your OTP is: {otp}",
                from_email="admin@example.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)


class VerifyRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        operation_description="Verify registration OTP"
    )

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                user = User.objects.get(email=email)
                email_otp = EmailOTP.objects.get(user=user)

            except (User.DoesNotExist, EmailOTP.DoesNotExist):
                return Response(
                    {"error": "Invalid email"},
                    status=400
                )

            if email_otp.is_expired():
                return Response(
                    {"error": "OTP expired"},
                    status=400
                )

            if email_otp.otp != otp:
                return Response(
                    {"error": "Invalid OTP"},
                    status=400
                )

            user.is_active = True
            user.save()

            email_otp.is_verified = True
            email_otp.save()

            return Response(
                {"message": "Registration verified successfully"},
                status=200
            )

        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login and set auth_token cookie"
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=400
                )

            user = authenticate(
                username=user_obj.username,
                password=password
            )

            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=400
                )

            token, created = Token.objects.get_or_create(user=user)

            response = Response(
                {"message": "Login successful"},
                status=200
            )

            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            return response

        return Response(serializer.errors, status=400)


class MeView(APIView):

    @swagger_auto_schema(
        operation_description="Get currently authenticated user"
    )

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class LogoutView(APIView):

    @swagger_auto_schema(
        operation_description="Logout and clear auth_token cookie"
    )

    def post(self, request):

        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass

        response = Response(
            {"message": "Logged out successfully"},
            status=200
        )

        response.delete_cookie('auth_token')

        return response