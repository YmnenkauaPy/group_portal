from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime
from django.shortcuts import render
from event import forms
from event import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def calendar(request):
    return render(request, 'group/calendar.html')

@login_required
def create_event(request, day_month_year):
    day_month_year = datetime.strptime(day_month_year, "%Y-%m-%d").date()

    if request.method == 'POST':
        form = forms.EventForm(request.POST, initial={'day_month_year': day_month_year}, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
        
            return redirect('calendar')
    else:
        form = forms.EventForm(initial={'day_month_year': day_month_year}, user=request.user)

    return render(request, 'group/create_event.html', {'form': form, 'day_month_year': day_month_year})

def get_event_data(request, day_month_year):
    try:
        date_object = datetime.strptime(day_month_year, '%Y-%m-%d').date()
        events = models.Event.objects.filter(
        Q(group__members=request.user) | Q(group__admin=request.user) | Q(group__moderators=request.user),
        day_month_year=date_object
        ).distinct()

        if events.exists():
            data = []
            for event in events:
                data.append({
                    'pk': event.pk,
                    'name': event.name,
                    'description': event.description,
                    'day_month_year': event.day_month_year.strftime('%Y-%m-%d'),
                    'time': event.time,
                    'group': {
                        'id': event.group.id,
                        'title': event.group.title
                    },
                })
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Event not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def role_is(request):
    role = 'member'
    if Q(group__admin=request.user) | Q(group__moderators=request.user):
        role='not member'
    return JsonResponse(role, safe=False)
  
def delete_event(request, pk):
    event = get_object_or_404(models.Event, pk=pk)

    if request.method == 'POST':
        event.delete() 
        return redirect('calendar') 

    return render(request, 'group/delete_event.html', {'event': event})

def edit_event(request, pk):
    event = get_object_or_404(models.Event, pk=pk)

    if request.method == 'POST':
        form = forms.EventForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()
            return redirect('calendar')
        else:
            print(form.errors)
    else:
        form = forms.EventForm(instance=event)

    return render(request, 'group/edit_event.html', {'form': form, 'event': event})

def events_for_month(request, year, month):
    events = models.Event.objects.filter(
        Q(group__members=request.user) | Q(group__admin=request.user) | Q(group__moderators=request.user),
        day_month_year__year=year)

    events_by_date = {}
    for event in events:
        event_date = event.day_month_year.strftime('%Y-%m-%d')
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append({
            'name': event.name,
            'description': event.description,
            'time': event.time.strftime('%H:%M'),
            'group': {
                'id': event.group.id,
                'title': event.group.title
            }
        })

    return JsonResponse(events_by_date)

