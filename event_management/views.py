from django.shortcuts import render

# Create your views here.
from .models import Event, Venue

def index(request):
    events = Event.objects.all()
    total_events = events.count()
    approved_events = events.filter(approval_status='approved').count()
    available_venues = Venue.objects.count()

    context = {
        'events': events,
        'total_events': total_events,
        'approved_events': approved_events,
        'available_venues': available_venues,
    }
    
    return render(request, 'index.html', context)