from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import User
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import Event
from events.serializers import EventSerializer

from django.contrib import messages



class CreateEvent(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)  
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400) 


class EventDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"message": "This event does not exist"},status=404)  

        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"message": "This event does not exist"}, status=404)

        if event.creator != request.user:
            return Response({"message": "Only the creator can update event"}, status=403)

        serializer = EventSerializer(event, data=request.data, partial=True) # allows updating specific fields without requiring all data.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"message": "You successfully updated this event"}, serializer.errors, status=400)
    
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"message": "This event does not exist"}, status=404)

        if event.creator != request.user:
            return Response({"message": "Only the creator can delete event"}, status=403)

        event.delete()
        return Response({"message": "You successfully deleted this event"}, status=204)     


class MyEventsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(creator=user)

    serializer_class = EventSerializer


class MyParticipationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        return user.participating_events.all()

    serializer_class = EventSerializer


class UserEventsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            print('not user')
            return Event.objects.none()  # Return empty queryset if no user_id provided

        try:
            user = User.objects.get(pk=user_id)
            return Event.objects.filter(creator=user)
        except User.DoesNotExist:
            print('user does not exist')
            return Event.objects.none() 
        
    serializer_class = EventSerializer
    

class EventListByLocation(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        location = user.profile.city  # Default to user's city

        # Get location and activity filters from query parameters
        location_param = self.request.query_params.get('location', None)
        activity_param = self.request.query_params.get('activity', None)

        queryset = Event.objects.all()
        
        if location:
            queryset = queryset.filter(location=location)

        # Filter by location parameter (if provided)
        if location_param:
            queryset = queryset.filter(location__name__icontains=location_param)

        # Filter by activity parameter (if provided)
        if activity_param:
            queryset = queryset.filter(activity__name__icontains=activity_param)

        return queryset
    
    serializer_class = EventSerializer


class JoinEvent(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer = EventSerializer

    def post(self, request, pk):

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"message": "This event does not exist"},status=404)

        user = request.user

        # Check if user is already participating
        if user in event.participants.all():
            return Response({"message": "You are already joined to this event"}, status=400)

        event.participants.add(user)
        event.save()

        return Response({"message":"You successfully joined the event"}, status=201)


class LeaveEvent(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"message": "This event does not exist"}, status=404)

        user = request.user

        # Check if user is participating
        if user not in event.participants.all():
            return Response({"message": "You are not currently joined to this event"}, status=400)

        if user == event.creator:
            return Response({"message": "You are the owner of this event and can not leave"}, status=400)
        
        event.participants.remove(user)
        event.save()

        return Response({"message": "You successfully left this event"},status=204) 
    

class TokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = RefreshToken.for_user(request.user)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response
