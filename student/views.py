import json
from random import choices
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
import os

from .models import studentlogin
from attendance.models import mark_attendance
import smtplib,secrets,string

from erp.models import subjects
from student.models import studentlogin
from .resources import StudentloginResource

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from erp.settings import password,sender
from import_export.formats import base_formats


def index(request):
    if request.user.is_active and request.user.groups.filter(name="student"). exists():
        return render(request,'dashboard.html')
    else:
        return render(request, 'studentlogin.html')

def login(request):
    if request.user.is_authenticated and request.user.groups.filter(name="student"). exists() :
        return index(request)
    elif request.method == 'POST':
        username = request.POST.get('studentid')
        password = request.POST.get('studentpwd')
        try:
            model_user = studentlogin.stud_obj.get(studentid=username,pwd=password)
            admin_user=authenticate(request, username=username, password=password)
            
            if model_user is not None:
                auth_login(request,admin_user)
                return HttpResponseRedirect('/student')
            else:
                messages.error(request, 'Invalid Credentials')
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return redirect('/student')
        except Exception as identifier:
            messages.error(request, 'Invalid Credentials')
            return redirect('/student')
    else:
        return render(request, 'studentlogin.html')

def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect('/student')

def attendance(request):
    if request.user.is_active and request.user.groups.filter(name="student").exists():
        student= studentlogin.stud_obj.get(studentid=request.user.username)
        attendance_list=mark_attendance.attend_obj.filter(student=student,semester=student.branch.semester)
        total=0
        total_present=0
        label={'Absent':[0,0]}
        for obj in attendance_list:
            if obj.present:
                if obj.subject in label:
                    label[obj.subject][0]+=1
                    label[obj.subject][1]+=1
                else:
                    label[obj.subject]=[1,1]
                total_present+=1
            else:
                if obj.subject in label:
                    label[obj.subject][1]+=1
                else:
                    label[obj.subject]=[0,1]
            total+=1
        label['Absent']=[total-total_present,total]
        
        colors=['red']
        
        for i in range(len(label)-1):
            temp='#'
            temp+=''.join(choices('0123456789ABCDEF',k=6))
            colors.append(temp)
        data={}
        data["labels"]=list(str(i) for i in label.keys())
        data['datasets']=dict([
            ('data',[i[0] for i in label.values()]),
            ('backgroundColor',colors)
            ])

        return render(request, 'stud_attendance.html',{"label":label,"total":[total_present,total],'data':json.dumps(data),'sem':student.branch.semester})

    else:
        return render(request,'studentlogin.html')

def timetable(request):
    if  request.user.is_active and studentlogin.stud_obj.filter(studentid=request.user.username):
        user = studentlogin.stud_obj.get(studentid=request.user.username)
        return render(request,"stud_timetable.html",{"user":user})
    else:
        return render(request,'studentlogin.html')

def subject(request):
    if request.user.is_active and studentlogin.stud_obj.filter(studentid=request.user.username):
        return render(request, 'dashboard.html')
    else:
        return render(request,'studentlogin.html')

def about(request):
    if request.user.is_active and studentlogin.stud_obj.filter(studentid=request.user.username):
        user = studentlogin.stud_obj.get(studentid=request.user.username)
        return render(request,"stud_about.html",{"user":user})
    else:
        return render(request,'studentlogin.html')

def forget(request):
	return render(request,'forget-password.html')

def forgot_mail(request):
    try:
        if request.method=='POST':
            user=studentlogin.stud_obj.get(email=request.POST.get('email'))

            letters = string.ascii_letters
            digits = string.digits
            special_chars = string.punctuation
            alphabet = letters + digits + special_chars
            pwd=''
            for _ in range(8):
                pwd += ''.join(secrets.choice(alphabet))
            setattr(user,'pwd',pwd)
            user.save()
            receiver=user.email
            user=user.Name
            user=user.title()
            email_body="Hello "+user+"\nYour password for erp portal is "+pwd+"\nThank you!"
            message=MIMEMultipart('alternative',None,[MIMEText(email_body,'text')])
            message['Subject']="Regarding ERP password"
            message['From']=sender
            message['To']=receiver
            try:
                server=smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(sender,password)
                server.sendmail(sender,receiver,message.as_string())
                server.quit()
            except:
                pass
        return login(request)
    except:
        messages.error(request, 'No user with this email found.')
        return forget(request)
    
def import_data(request):
    if request.method == 'POST':
        resource = StudentloginResource()
        dataset = base_formats.XLSX()
        imported_data = request.FILES['file'].read()
        result = resource.import_data(imported_data, dry_run=True)  # Test the data import
        if not result.has_errors():
            resource.import_data(imported_data,dry_run= False)  # Actually import now
    return render(request, 'import_data.html')