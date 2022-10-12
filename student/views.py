from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login,authenticate
from .models import studentlogin

def index(request):
    return render(request,'studentlogin.html')
    #return render_to_response('home.html')
# Create your views here.
def login(request):
        if request.method == 'POST':
            username = request.POST.get('studentid')
            password = request.POST.get('studentpwd')
            try:
                user = studentlogin.stud_obj.get(studentid=username,studentpwd=password)
                if user is not None:
                    return render(request, 'dashboard.html', {})
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
                    return redirect('/student')
            except Exception as identifier:
                return redirect('/student')
        else:
            return render(request, 'studentlogin.html')
