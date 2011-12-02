from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# View function for homepage
def home(request):
    #Render the view to the index.html template
    return render_to_response('index.html', {}, context_instance=RequestContext(request))