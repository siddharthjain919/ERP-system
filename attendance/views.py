from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import mark_attendance
from .forms import mark_attendance_form
from django.contrib.auth.models import User
from datetime import datetime,timedelta
# from django.urls import reverse
from django.contrib import messages
from erp.models import *
from branch.models import *
from student.models import studentlogin
from teacher.models import teacherlogin
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
        unique_branch=[]
        for i in branches:
            if i.name not in unique_branch:
                unique_branch.append(i.name)
        return render(request,'load_branch_dropdown_list.html',{'branches':unique_branch})
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
            curr_group=request.POST.get("group")
            if curr_group=="Both":
                student_list=list(User.objects.filter(groups__name=curr_branch))
            else:
                student_list=list(User.objects.filter(groups__name=str(curr_branch)+"_"+curr_group))
            sos=[]
            for i in "12345":
                so=i+getattr(curr_subject,"CO_"+i)
                sos.append(so)
            return render(request,"attendancelist.html",context={"sos":sos,"student_list":student_list,"curr_branch":curr_branch,"curr_subject":curr_subject,"group":curr_group})
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')

def mark(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        if request.method=='POST':
            #form input
            subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
            lecture_list=request.POST.getlist("lecture_no")
            topic_list=request.POST.getlist("topics")
            topic_list={"topics":topic_list}
            date=request.POST.get('date')
            date=datetime.strptime(date,"%Y-%m-%d").date()
            branch=request.POST.get("branch")
            group=request.POST.get("group")

            #marking attendance
            if group=="Both":
                branch=User.objects.filter(groups__name=branch)
            else:
                branch=User.objects.filter(groups__name=str(branch)+"_"+group)
            teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
            branchSubject=branch_subjects.branch_sub_obj.get(subject_teacher=teacher,branch_subject=subject)
            objective=request.POST.get("so")
            setattr(branchSubject,"NOLT"+str(objective),getattr(branchSubject,"NOLT"+str(objective))+1)
            branchSubject.save()
            # print(branchSubject.NOLT2)
            error=0
            for lecture_number in lecture_list:
                
                for i in branch:
                    student=studentlogin.stud_obj.get(studentid=i)
                    previous_check=mark_attendance.attend_obj.filter(date=date,lecture_number=lecture_number,semester=student.branch.semester)
                    if len(previous_check):
                        messages.info(request,"Attendance already exists for lecture "+lecture_number+" by "+previous_check[0].teacher.Name+'('+previous_check[0].teacher.teacherid+')')
                        error+=1
                        break 
                else:
                    lecture_number=int(lecture_number)
                    messages.success(request,"Attendance marked for lecture "+str(lecture_number)+" successfully.")
                    for i in branch:
                        student=studentlogin.stud_obj.get(studentid=i)
                        previous_check=mark_attendance.attend_obj.filter(date=date,lecture_number=lecture_number,semester=student.branch.semester)
                        if str(i)+'_exempt' in request.POST:
                            continue
                        elif str(i) in request.POST:
                            mark_attendance.attend_obj.create(student=student,subject=subject,present=True,date=date,lecture_number=lecture_number,semester=student.branch.semester,session=student.branch.batch,teacher=teacher,topics=topic_list)
                        else:
                            mark_attendance.attend_obj.create(student=student,subject=subject,present=False,date=date,lecture_number=lecture_number,semester=student.branch.semester,session=student.branch.batch,teacher=teacher,topics=topic_list)
            
            #marking lds
            lecturenumber=branchSubject.NOLT1+branchSubject.NOLT2+branchSubject.NOLT3+branchSubject.NOLT4+branchSubject.NOLT5
            

            return HttpResponseRedirect("/teacher/attendance/")
        else:
            return attendance_form(request)
    else:
        return redirect('/teacher/login')

def pastattendance(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():

        branch=request.GET.get('branch')
        semester=request.GET.get('semester')
        date_from=request.GET.get('date_from')
        date_to=request.GET.get('date_to')
        session=request.GET.get('session')
        studentid=request.GET.get('studentid')

        teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
        print(teacher,type(teacher))

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
                attendancelist=list(mark_attendance.attend_obj.all())
                return render(request,"load_studentlist.html",{"branches":branches,"attendancelist":attendancelist})
        if semester:
            query&=Q(semester=semester)
        if date_from and date_to and date_from<=date_to:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            step=timedelta(days=1)
            dateQ=Q()
            while date_from<=date_to:
                dateQ|=Q(date=date_from)
                date_from+=step
            if dateQ:
                query&=dateQ

        if session:
            query&=Q(session=session)
        if branch and branch!='None':
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
            print(query)
            query&=Q(teacher=teacher)
            attendancelist=list(mark_attendance.attend_obj.filter(query))
            return render(request,"load_studentlist.html",{"branches":branches,"attendancelist":attendancelist})
        else:
            attendancelist=list(mark_attendance.attend_obj.filter(teacher=teacher))
            return render(request,"pastattendance.html",{"branches":branches,"attendancelist":attendancelist})
    else:
        return redirect('/teacher/login')
    

def load_topics(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        so=request.GET.get('so')
        subject=request.GET.get('subject')
        print(subject)
        subject=subjects.sub_obj.get(subject_name=subject)
        topics_list=getattr(subject,"topics"+so)["topic_list"]
        
        return render(request,'load_topics.html',{"topics_list":topics_list})
    else:
        return redirect('/teacher/login')


