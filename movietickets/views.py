from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status,viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def list(self, request, pk=None):
        try:
            serializer = MovieSerializer(self.queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def list(self, request, pk=None):
        try:
            serializer = TicketSerializer(self.queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

