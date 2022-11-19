from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import studentlogin


def index(request):
    if not request.user.is_active:
        return render(request,'login.html')
    else:
        return render(request, 'dashboard.html', {})
    #return render_to_response('home.html')

def login(request):
    if request.user.is_active:
        return index(request)
    elif request.method == 'POST':
        username = request.POST.get('studentid')
        password = request.POST.get('studentpwd')
        try:
            model_user = studentlogin.stud_obj.get(studentid=username,studentpwd=password)
            admin_user=authenticate(request, username=username, password=password)
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
