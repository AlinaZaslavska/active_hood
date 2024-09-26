# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EventForm
from .models import Event
from django.contrib import messages
from users.models import Activity, User
from locations.models import City


@login_required
def events_list(request):
    user = request.user
    location = user.profile.city  
    
    # Get location and activity filters from query parameters
    location_param = request.GET.get('location', None)
    activity_param = request.GET.get('activity', None)
    
    queryset = Event.objects.all()

    # Prioritize user-specified location
    if location_param:
        queryset = queryset.filter(location__name__icontains=location_param)
    elif location:
        queryset = queryset.filter(location=location)

    activities = Activity.objects.all()
    locations = City.objects.all()
    events = queryset

    return render(request, 'events/events_list.html', {
        'events': queryset,
        'activities': activities,
        'locations': locations,
    })


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('events_myevents')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_is_creator = event.creator == request.user
    user_is_participant = request.user in event.participants.all()
    user_city = request.user.profile.city 

    context = {
        'event': event,
        'user_is_creator': user_is_creator,
        'user_is_participant': user_is_participant,
        'user_city': user_city,
    }

    return render(request, 'events/event_detail.html', context)


@login_required
def my_events(request):
    events = Event.objects.filter(creator=request.user)
    deleted = request.GET.get('deleted')
    if deleted:
        messages.success(request, "Event deleted successfully.")
    return render(request, 'events/my_events.html', {'events': events})


@login_required
def participating(request):
    events = request.user.participating_events.all()
    return render(request, 'events/participating.html', {'events': events})


@login_required
def user_events(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    events = Event.objects.filter(creator=user)
    return render(request, 'events/user_events.html', {'events': events})


@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user == event.creator:
        messages.error(request, "You are the owner of this event and cannot join it.")
    elif request.user in event.participants.all():
        messages.error(request, "You are already joined to this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "You successfully joined the event.")
    
    return redirect('event_detail', pk=pk)


@login_required
def leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user == event.creator:
        messages.error(request, "You are the owner of this event and cannot leave it.")
    elif request.user not in event.participants.all():
        messages.error(request, "You are not currently joined to this event.")
    else:
        event.participants.remove(request.user)
        messages.success(request, "You successfully left the event.")
    
    return redirect('event_detail', pk=pk)


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.creator != request.user:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('event_detail', pk=pk)

    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('events_myevents')  