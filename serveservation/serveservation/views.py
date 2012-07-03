# Create your views here.
#from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from servers.models import Server
#from django.http import Http404 #jg
#from django.shortcuts import render_to_response, get_object_or_404

#def index(request):
  #all_servers_list = Server.objects.all()
  #t = loader.get_template('servers/index.html')
  #c = Context({
      #'all_servers_list' : all_servers_list,
  #})
  #return HttpResponse(t.render(c))

def home(request):
  return render_to_response('index.html' )
  
def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('serveservation/error404.html', {'serveservation': p})