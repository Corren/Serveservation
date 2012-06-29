# Create your views here.
#from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from servers.models import Server, Reservation
from servers.forms import ServerForm, ReservationForm

def server_page(request, servername):
  server = Server.objects.get(name=servername)
  reservations = Reservation.objects.filter(server=server).exclude(reserved_by=None)
  return render_to_response('servers/server.html', { 'server' : server, 'reservations' : reservations })

def all_servers(request):
  all_servers_list = Server.objects.all()
  return render_to_response('servers/index.html', {'all_servers_list' : all_servers_list} )

def reservations(request):
  all_reservations = Reservation.objects.all()
  return render_to_response('reservations/index.html', {'all_reservations' : all_reservations})

def reserve_server(request):
  ReserveFormSet = modelformset_factory(Reservation)
  if request.method == 'POST':
    formset = ReserveFormSet(request.POST, request.FILES)
    if formset.is_valid():
      formset.save()
  else:
    formset = ReserveFormSet()
  return render_to_response('reservations/reserve.html', { 'formset' : formset })
