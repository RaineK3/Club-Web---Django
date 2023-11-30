from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Venue
from .forms import VenueForm,EventForm
from django.http import HttpResponse
import csv

#generate csv file venue list
def venue_csv(request):
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'

	#create a csv writer
	writer = csv.writer(response)

	#designate the model
	venues = Venue.objects.all()

	#add column headings to the csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web', "Email"])

	#loop through and output
	for venue in venues:
		writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])

	return response

def venue_text(request):
	response = HttpResponse(content_type = 'text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'
	# lines = ['This is line\n',
	# "This is line 2\n"]

	# #write to textfile
	# response.writelines(lines)
	# return response

	#designate the model
	venues = Venue.objects.all()
	#create empty list
	lines = []
	#loop through and output
	for venue in venues:
		lines.append(f'Venue Name: {venue.name}\nAddress: {venue.address}\nPhone: {venue.phone}\nWebsit: {venue.web}\nEmail:{venue.email_address}\n\n')

	response.writelines(lines)
	return response

def delete_venue(request, venue_id):
	event = Venue.objects.get(pk = venue_id)
	event.delete()
	return redirect('list-venues')

def delete_event(request, event_id):
	event = Event.objects.get(pk = event_id)
	event.delete()
	return redirect('list-events')

def add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_event?submitted=Ture')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	
	return render(request, 'events/add_event.html',
		{'form': form, 'submitted': submitted})

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance = event)
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'events/update_event.html',
		{'event': event,
		'form' : form})

def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance = venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')

	return render(request, 'events/update_venue.html',
		{'venue': venue,
		'form' : form})

def search_venues(request):
	if request.method == "POST":
		#getting data from search input field
		searched = request.POST['searched']
		#getting venue objects by filtering name with searched
		venues = Venue.objects.filter(name__contains =searched)  
		return render(request, 'events/search_venues.html',
			{'searched': searched,
			'venues': venues})
	else:
		return render(request, 'events/search_venues.html',
			{})

def show_venue(request,  venue_id):
	venue = Venue.objects.get(pk = venue_id)
	return render(request, 'events/show_venue.html',
		{'venue': venue})

def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')
	return render(request, 'events/venue.html',
		{'venue_list': venue_list})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=Ture')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	
	return render(request, 'events/add_venue.html',
		{'form': form, 'submitted': submitted})

def all_events(request):
	event_list = Event.objects.all().order_by('name')
	return render(request, 'events/event_list.html',
		{'event_list':event_list})

def home(request,year = datetime.now
	().year ,month=datetime.now().strftime('%B')):
	name = "Liadrin"
	month = month.title()
	#convert month form name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	#create a calendar
	cal = HTMLCalendar().formatmonth(
		year,
		month_number)

	#getting current year
	now = datetime.now()
	current_year = now.year
	#get current time
	time = now.strftime('%H:%M:%S %p')
	return render(request,"events/home.html",{
		"name":name,
		"year":year,
		"month":month,
		"month_number" : month_number,
		"cal" : cal, 
		"current_year" : current_year,
		"time" : time,
		})
