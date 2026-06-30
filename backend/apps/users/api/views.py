from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True,
        )
        user = serializer.save()

        response_serializer = UserSerializer(user)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
    

class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )
        user = serializer.validated_data['user']

        return Response(
            {
                "user": UserSerializer(user).data,
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
            },
            status=status.HTTP_200_OK,
        )
    


class MeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
