from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from rest_framework import status
from django.contrib.auth.models import User

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({
            #     "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            #     "message": "User Created Successfully.  Now perform Login to get your token",
            # })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

