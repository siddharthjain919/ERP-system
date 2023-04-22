import json
from random import choices
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from import_export.formats import base_formats

from erp.services import create_new_password
from branch.services import get_subjects_by_branch

from .models import studentlogin
from .services import get_student_by_user
from attendance.models import mark_attendance
from .resources import StudentloginResource
from branch.services import get_subjects_by_branch,get_labs
from erp.services import get_subject



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
    if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
        student= get_student_by_user(request.user.username)
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
        allcolors = ['#3D9970', '#39CCCC', '#2ECC40', '#0074D9', '#7FDBFF', '#B10DC9', '#85144b', '#F012BE', '#DDDDDD', '#111111', '#AAAAAA', '#001f3f', '#0074D9', '#FF851B', '#FFDC00', '#3D9970', '#2ECC40']
        colors=colors+choices(allcolors,k=len(label)-1)
        for i in range(len(label)-1):
            temp=choices(allcolors,k=1)[0]
            allcolors.remove(temp)
            colors.append(temp)
        
        # for i in range(len(label)-1):
        #     temp='#'
        #     temp+=''.join(choices('0123456789ABCDEF',k=6))
        #     colors.append(temp)
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
    if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
        user = get_student_by_user(request.user.username)
        return render(request,"stud_timetable.html",{"user":user})
    else:
        return render(request,'studentlogin.html')

def subject(request):
    if  request.user.is_authenticated and request.user.groups.filter(name="student").exists():
        student=get_student_by_user(request.user.username)
        subjects=get_subjects_by_branch(student.branch)
        return render(request, 'stud_subjects.html',{'subjects':subjects,"sem":student.branch.semester})
    else:
        return render(request,'studentlogin.html')

def about(request):
    if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
        user = get_student_by_user(request.user.username)
        return render(request,"stud_about.html",{"user":user})
    else:
        return render(request,'studentlogin.html')

def forget(request):
	return render(request,'forget-password.html')

def forgot_mail(request):
    try:
        if request.method=='POST':
            user=studentlogin.stud_obj.get(email=request.POST.get('email'))
            create_new_password(user)
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

def lab_simulator(request):
    if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
        user = get_student_by_user(request.user.username)
        if request.method=='POST':
            # return render(request,"lab_compiler.html",{"user":user,'subject':subject})
            pass
        else:
            try:
                subject=request.GET.get('subject')
                branch=user.branch
                subject=get_subject(subject)
                return render(request,"lab_compiler.html",{"user":user,'subject':subject})
            except:
                subjects=get_subjects_by_branch(user.branch)
                # print(subjects)
                subjects=get_labs(subjects)
                # print(subjects)
                return render(request,'lab_subjects.html',{'subjects':subjects})

    else:
        return render(request,'studentlogin.html')