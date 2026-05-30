from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SignupSerializer, LoginSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({
                "message": "로그인 성공",
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)