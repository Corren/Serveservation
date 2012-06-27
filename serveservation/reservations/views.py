# Create your views here.
#from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reservations.models import Server

#def index(request):
  #all_servers_list = Server.objects.all()
  #t = loader.get_template('reservations/index.html')
  #c = Context({
      #'all_servers_list' : all_servers_list,
  #})
  #return HttpResponse(t.render(c))

def index(request):
  all_servers_list = Server.objects.all()
  return render_to_response('reservations/index.html', {'all_servers_list' : all_servers_list})
