from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status,viewsets, filters, generics
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from .serializers import *

# Create your views here.

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        items = User.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieSearchAPIView(generics.ListAPIView):
    search_fields = ['name', 'description', 'cast', 'trailer', 'director']
    filter_backends = (filters.SearchFilter,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    @action(detail=False, methods=["get"])
    def get_movie(self, request, format=None):
        try:
            movie_id = request.GET["movie_id"]
            movie = Movie.objects.get(id=movie_id)
            return Response(MovieSerializer(movie).data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

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

    @action(detail=True, methods=["put"])
    def purchase_ticket(self, request, pk, format=None):
        ticket = Ticket.objects.get(pk=pk)
        ticket.user = request.user
        ticket.save()
        serializer = TicketSerializer(data=request.data)
        return JsonResponse({"status": "success"})

    @action(detail=False, methods=["get"])
    def get_my_tickets(self, request, pk=None):
        try:
            q = Q(user=request.user)
            queryset = self.queryset.filter(q)
            serializer = TicketSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({"error": str(e)})