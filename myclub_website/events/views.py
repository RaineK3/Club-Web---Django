from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Venue
from .forms import VenueForm,EventForm, EventFormAdmin
from django.http import HttpResponse
import csv

#for generate pdf stuff
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#import pagination stuff
from django.core.paginator import Paginator

#generate a PDF File Venue List
def venue_pdf(request):
	#create bytestream buffer
	buf = io.BytesIO()
	#create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup = 0)
	#create text object 
	textob = c.beginText()
	textob.setTextOrigin(inch,inch)
	textob.setFont("Helvetica", 14)

	#add some line of text
	# lines = [
	# "This is line 1",
	# "Thid is line 2",
	# "This is line 3",
	# "This is line 4"]

	#designate the model
	venues = Venue.objects.all()

	#create blank list
	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")

	#loop
	for line in lines:
		textob.textLine(line)


	#Finish up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	#return something
	return FileResponse(buf, as_attachment= True, filename="venue.pdf")

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
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=Ture')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				# form.save()
				event = form.save(commit = False)
				event.manager = request.user 
				event.save()
				return HttpResponseRedirect('/add_event?submitted=Ture')
	else:
		#just going to the page, not submitting
		if request.user.is_superuser:
			form = EventFormAdmin
		else: 
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	
	return render(request, 'events/add_event.html',
		{'form': form, 'submitted': submitted})

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance = event)
	else:
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
	#venue_list = Venue.objects.all().order_by('name')
	venue_list = Venue.objects.all()

	#set up pagination
	p = Paginator(Venue.objects.all(), 	1)
	page = request.GET.get('page')
	venues = p.get_page(page)

	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/venue.html',
		{'venue_list': venue_list,
		'venues': venues,
		'nums': nums })

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			#form.save()
			venue = form.save(commit = False)
			venue.owner = request.user.id #logged in user
			venue.save()			# form.save()
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
