from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    d={'insert':"hello buddy"}
    return render(request,'homepage/home.html',context=d)
    #return render_to_response('home.html')

    #return HttpResponse(template.render(request))
# Create your views here.
