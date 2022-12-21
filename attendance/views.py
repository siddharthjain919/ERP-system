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
from django.db.models import Q
# Create your views here.

def attendance_form(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        form=mark_attendance_form()
        return render(request,'attendance.html',context={"form":form})
    else:
        return redirect('/teacher/login')
    
def load_branch_details(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        curr_course=course.course_obj.get(name=request.GET.get('course'))
        curr_batch=request.GET.get('batch')
        branches=list(branch_detail.branch_obj.filter(course=curr_course,batch=curr_batch))
        return render(request,'load_branch_dropdown_list.html',{'branches':branches})
    else:
        return redirect('/teacher/login')

def load_subject_details(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        curr_branch=branch_detail.branch_obj.get(name=request.GET.get('branch'),batch=request.GET.get('batch'),section=request.GET.get('section'))
        subjects=list(branch_subjects.branch_sub_obj.filter(branch=curr_branch))
        students=list(studentlogin.stud_obj.filter(branch=curr_branch))
        return render(request,'load_subject_dropdown_list.html',{'subjects':subjects,'students':students})
    else:
        return redirect('/teacher/login')

def studentlist(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        if request.method=='POST':
            curr_branch=branch_detail.branch_obj.get(name=request.POST.get('branch'),batch=request.POST.get('batch'),section=request.POST.get('section'))
            curr_subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
            student_list=list(User.objects.filter(groups__name=curr_branch))
            sos=[]
            for i in "12345":
                so=i+getattr(curr_subject,"CO_"+i)
                sos.append(so)
            return render(request,"studentlist.html",context={"sos":sos,"student_list":student_list,"curr_branch":curr_branch,"curr_subject":curr_subject})
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')

def mark(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        if request.method=='POST':
            print(list(request.POST.items()))
            subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
            lecture_number=request.POST.get("lecture_no")
            date=request.POST.get('date')
            date=datetime.strptime(date,"%Y-%m-%d").date()
            branch=request.POST.get("branch")
            branch=User.objects.filter(groups__name=branch)
            for i in branch:
                student=studentlogin.stud_obj.get(studentid=i)
                if str(i)+'_exempt' in request.POST:
                    continue
                elif str(i) in request.POST:
                    mark_attendance.attend_obj.create(student=student,subject=subject,present=True,date=date,lecture_number=lecture_number,semester=student.branch.semester,session=student.branch.batch)
                else:
                    mark_attendance.attend_obj.create(student=student,subject=subject,present=False,date=date,lecture_number=lecture_number,semester=student.branch.semester,session=student.branch.batch)
            return HttpResponseRedirect("/teacher/attendance/")
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')

def pastattendance(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        branch=request.GET.get('branch')
        semester=request.GET.get('semester')
        date=request.GET.get('date')
        session=request.GET.get('session')
        studentid=request.GET.get('studentid')
        branches=branch_detail.branch_obj.all()
        query=Q()
        if studentid:
            try:
                studentid=studentid.upper()
                studentid=studentlogin.stud_obj.get(studentid=studentid)
                query&=Q(student=studentid)
            except:
                messages.add_message(request, messages.SUCCESS, 'Invalid Student Id!')
                query=Q()
        if semester:
            query&=Q(semester=semester)
        if date:
            query&=Q(date=date)
        if session:
            query&=Q(session=session)
        if branch:
            temp=branch
            branch=branch.split('-')
            batch=int(branch[1])
            branch=branch[0].split('(')
            section=branch[1][0]
            branch=branch[0]
            branch=branch_detail.branch_obj.get(name=branch,batch=batch,section=section)
            studentlist=studentlogin.stud_obj.filter(branch=branch)
            attendancelist=[]
            query2=Q()
            for student in studentlist:
                query2|=Q(student=student)

            attendancelist=list(mark_attendance.attend_obj.filter(query&query2))
            return render(request,"load_studentlist.html",{"branches":branches,"attendancelist":attendancelist})

        elif query:
            attendancelist=list(mark_attendance.attend_obj.filter(query))
            return render(request,"load_studentlist.html",{"branches":branches,"attendancelist":attendancelist})
        else:
            attendancelist=list(mark_attendance.attend_obj.all())
            return render(request,"pastattendance.html",{"branches":branches,"attendancelist":attendancelist})
