"""
Views de autenticación: Enrutadores que delegan la lógica a AuthenticationController.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, OTPVerifySerializer, UserProfileSerializer
from .controllers import AuthenticationController
from .services import OTPService
from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import AuditLogService


class LoginView(APIView):
    """Inicio de sesión (Router)"""
    permission_classes = [AllowAny]
    throttle_scope = 'login'

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        if user.is_2fa_enabled:
            otp = OTPService.generate_and_send(user)
            AuditLogService.log(
                user=user,
                action=AuditLog.Action.LOGIN_OTP_SENT,
                request=request,
            )
            return Response({
                'requires_2fa': True,
                'temp_token': str(otp.temp_token),
                'message': 'Código OTP enviado al correo institucional.',
            }, status=status.HTTP_200_OK)

        tokens = AuthenticationController.process_direct_login(user, request)

        return Response({
            'requires_2fa': False,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': UserProfileSerializer(user).data,
            'message': 'Inicio de sesión exitoso.',
        }, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    """Verificación de OTP (Router)"""
    permission_classes = [AllowAny]
    throttle_scope = 'login'

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data['otp']
        user = serializer.validated_data['user']

        tokens = AuthenticationController.process_otp_login(user, otp, request)

        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': UserProfileSerializer(user).data,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Cerrar sesión (Router)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            AuthenticationController.process_logout(request.user, refresh_token, request)
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """Perfil del usuario (Router)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)
