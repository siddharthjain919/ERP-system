from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import mark_attendance
from .forms import mark_attendance_form
from django.contrib.auth.models import User
from datetime import datetime
# from django.urls import reverse
from django.contrib import messages
from erp.models import *
from branch.models import *
from student.models import studentlogin
# Create your views here.

def attendance_form(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        # course_list=list(course.course_obj.all())
        # department_list=[]
        # branch_list=[]
        form=mark_attendance_form()
        return render(request,'attendance.html',context={"form":form})
    else:
        return redirect('/teacher/login')

def load_department_details(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        curr_course=course.course_obj.get(name=request.GET.get('course'))
        departments=list(department.department_obj.filter(course=curr_course))
        return render(request,'load_department_dropdown_list.html',{'departments':departments})
    else:
        return redirect('/teacher/login')
    
def load_branch_details(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        curr_dept=department.department_obj.get(name=request.GET.get('department'))
        branches=list(branch_detail.branch_obj.filter(department=curr_dept))
        return render(request,'load_branch_dropdown_list.html',{'branches':branches})
    else:
        return redirect('/teacher/login')

def load_subject_details(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        curr_branch=branch_detail.branch_obj.get(name=request.GET.get('branch'))
        subjects=list(branch_subjects.branch_sub_obj.filter(branch=curr_branch))
        students=list(studentlogin.stud_obj.filter(branch=curr_branch))
        return render(request,'load_subject_dropdown_list.html',{'subjects':subjects,'students':students})
    else:
        return redirect('/teacher/login')

def studentlist(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        if request.method=='POST':
            curr_branch=branch_detail.branch_obj.get(name=request.POST.get('branch'))
            curr_subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
            student_list=list(User.objects.filter(groups__name=curr_branch))
            sos=[]
            for i in "12345":
                so=i+getattr(curr_subject,"Objective_"+i)
                sos.append(so)
            # return attendance_form(request)
            return render(request,"studentlist.html",context={"sos":sos,"student_list":student_list,"curr_branch":curr_branch,"curr_subject":curr_subject})
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')

def mark(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        if request.method=='POST':
            subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
            lecture_number=request.POST.get("lecture_no")
            date=request.POST.get('date')
            date=datetime.strptime(date,"%Y-%m-%d").date()
            branch=request.POST.get("branch")
            branch=User.objects.filter(groups__name=branch)
            for i in branch:
                student=studentlogin.stud_obj.get(studentid=i)
                if student.studentid in request.POST:
                    mark_attendance.attend_obj.create(student=student,subject=subject,present=True,date=date,lecture_number=lecture_number)
                else:
                    mark_attendance.attend_obj.create(student=student,subject=subject,present=False,date=date,lecture_number=lecture_number)
            return HttpResponseRedirect("/teacher/attendance/")
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')