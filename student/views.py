from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
# import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from .models import studentlogin
from attendance.models import mark_attendance
import smtplib,secrets,string
from erp.models import subjects
from student.models import studentlogin
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from erp.settings import password,sender


def index(request):
    if request.user.is_active and request.user.groups.filter(name="student"). exists():
        return render(request,'dashboard.html')
    else:
        return render(request, 'studentlogin.html')
    #return render_to_response('home.html')

def login(request):
    if request.user.is_authenticated and request.user.groups.filter(name="student"). exists() :
        return index(request)
    elif request.method == 'POST':
        username = request.POST.get('studentid')
        password = request.POST.get('studentpwd')
        try:
            model_user = studentlogin.stud_obj.get(studentid=username,studentpwd=password)
            admin_user=authenticate(request, username=username, password=password)
            if model_user is not None:
                auth_login(request,admin_user)
                return render(request, 'dashboard.html', {})
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
        attendance_list=mark_attendance.attend_obj.filter(student=student)
        print(attendance_list)
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
        fig1,ax1=plt.subplots()
        # ,explode=(0.025,)*len(label)
        ax1.pie([i[0] for i in label.values()],labels=tuple(label.keys()),explode=(0.0125,)*len(label),autopct='%1.1f%%',startangle=90,pctdistance=0.65)
        centre_circle=plt.Circle((0,0),0.82,fc='white')
        fig=plt.gcf()
        try:
            plt.text(-.125, 0,str(round(total_present/total*100,2))+'%')
        except:
            plt.text(-.125, 0,'No Record Found')
        plt.xlim([-4, 4])
        plt.ylim([-4, 4])
        fig.gca().add_artist(centre_circle)
        ax1.axis('equal')
        # WHEN DEPLOYMENT
        # try:
        #     os.remove('ERP/media/'+str(student)+'.png')
        # except:
        #     pass
        # plt.savefig('ERP/media/'+str(student)+'.png',format="png",dpi=500)
        try:
            os.remove('media//'+str(student)+'.png')
        except:
            pass
        plt.savefig('media//'+str(student)+'.png',dpi=500)
        return render(request, 'stud_attendance.html',{"label":label,"total":[total_present,total]})
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
        return render(request, 'dashboard.html')
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
            setattr(user,'teacherpwd',pwd)
            # user2=User.objects.get(username=user.teacherid)
            # setattr(user2,'password',pwd)
            # user2.save()
            #for adding user to group
            user.save()
            #sending mails
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