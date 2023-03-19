import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

from .extras import *

from branch.models import branch_detail, branch_subjects
from branch.forms import branch_subject_form
from erp.models import subjects,question_paper
from student.models import studentlogin,student_marks
from .models import teacherlogin


def index(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():

		teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
		subject_list=list(branch_subjects.branch_sub_obj.filter(subject_teacher=teacher))
		
		lectures=[]
		today = datetime.date.today()
		today=today.strftime("%A").lower()[:-3]
		if today=="wednes" or today=="satur":
			today=today[:3]
		current_time = datetime.datetime.now().time()
		current_time=int(current_time.hour)*60+int(current_time.minute)
		# current_time=550
		emoji = "\U0001F610"
		if current_time<940 and today!='sun':
			if current_time>=840:
				current_time-=60
			elif current_time>=640:
				current_time-=10
			current_time-=530
			n=current_time//50+1
			if n>0 and n<9:
				current_lecture=getattr(teacher,"teach_"+today+"_lec"+str(n))
				print(type(current_lecture))
				if current_lecture:
					lectures.append("In "+str(current_lecture)+" now.")
			n=max(0,n)
			for i in range(n+1,9):
				temp=getattr(teacher,"teach_"+today+"_lec"+str(i))
				if temp:
					lectures.append("In "+str(temp)+" in lecture "+str(i)+'.')
		if not len(lectures):
			emoji = "\U0001F63B"
			lectures.append("Free for the day")
		print(lectures)

		return render(request, 'dash1.html', {"subject_list":subject_list,"lectures":lectures,"emoji":emoji})
	else:
		return render(request,'login.html')

def login(request):
	if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
		return index(request)
	elif request.method == 'POST':
		username = request.POST.get('teacherid')
		password = request.POST.get('teacherpwd')
		try:
			user = teacherlogin.teach_obj.get(teacherid=username,pwd=password)
			# print(user)
			user2 = authenticate(request, username=username, password=password)
			if user is not None:
				auth_login(request,user2)
				return HttpResponseRedirect('/teacher')
			else:
				messages.error(request, 'Invalid Credentials')
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username,password))
				return redirect('/')
		except Exception as identifier:
			messages.error(request, 'Invalid Credentials')
			print("******\n",identifier,1,"\n******",46)
			return redirect('/teacher')
	
	else:
		return render(request,'login.html')

def logout(request):
	request.session.flush()
	auth_logout(request)
	return redirect('/teacher/login')

def timetable(request):
	if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
		if request.method=='POST':
			branch=request.POST.get("cc_branch").split('-')
			name=branch[0].split('(')
			section=name[1][0]
			name=name[0]
			batch=int(branch[1])
			branch=branch_detail.branch_obj.get(name=name,section=section,batch=batch)
			for i in ['mon','tues','wed','thurs','fri','sat']:
				for j in range(1,9):
					lecture_name=i+'_lec'+str(j)
					lecture_input=request.POST.get(lecture_name)
					# print(1,lecture_input,type(lecture_input))
					previous=getattr(branch,lecture_name)
					# print(lecture_input,previous)
					# print(2,previous,type(previous))
					# print(lecture_input,previous,type(lecture_input),11111111111111)
					if lecture_input=='':
						continue
					if lecture_input:
						lecture_input=lecture_input.split('-')
						subject_name=lecture_input[0]
						subject_name=subjects.sub_obj.get(subject_name=subject_name)
						subject_teacher=lecture_input[1]
						subject_teacher=teacherlogin.teach_obj.get(name=subject_teacher)
						teacher_slot=getattr(subject_teacher,"teach_"+lecture_name)
						if teacher_slot and teacher_slot!=branch:
							raise Exception(subject_teacher.name,"already occupied at",lecture_name)
						if previous and lecture_input!=previous:
							setattr(previous.subject_teacher,"teach_"+lecture_name,None)
							previous.subject_teacher.save()
							messages.info(request,"cleared {0} from {1} at slot {2}".format(branch,previous.subject_teacher.name,lecture_name))
						setattr(subject_teacher,"teach_"+lecture_name,branch)
						subject_teacher.save()
						# print(getattr(subject_teacher,"teach_"+lecture_name,55555555555555555555))
						setattr(branch,lecture_name,branch_subjects.branch_sub_obj.get(subject_teacher=subject_teacher,branch_subject=subject_name,branch=branch))
					elif previous:
						setattr(previous.subject_teacher,"teach_"+lecture_name,None)
						previous.subject_teacher.save()
						setattr(branch,lecture_name,None)
					else:
						setattr(branch,lecture_name,None)
					branch.save()
		
		teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
		cc_branch=teacher.cc_of_branch
		# print(request.user,teacher,cc_branch)
		branch_list=list(branch_detail.branch_obj.all())
		if cc_branch:
			branch_list.remove(cc_branch)
			subject_list=list(branch_subjects.branch_sub_obj.filter(branch=cc_branch))
		else:
			subject_list=[]
		return render(request,'timetable.html',context={"branch_list":branch_list,"subject_list":subject_list,"cc_branch":cc_branch,"user": request.user})
	else:
		return redirect('/teacher/login')

def subject(request):
	if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
		if request.method=="POST":
			form=branch_subject_form(request.POST)
			if form.is_valid():
				form.save()
			request.method="GET"
			return subject(request)
		else:
			current_branch=teacherlogin.teach_obj.get(teacherid=request.user.username).branch
			subject_list=list(branch_subjects.branch_sub_obj.all())
			form=branch_subject_form()
			return render(request,'subjects.html',context={"form":form,'branch_subject':subject_list})
	else:
		return redirect('/teacher/login')

def about(request):
	if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
		user = teacherlogin.teach_obj.get(teacherid=request.user.username)
		return render(request,"about.html",{"user":user})
	else:
		return redirect('/teacher/login')

def teachertimetable(request):
	if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
		user = teacherlogin.teach_obj.get(teacherid=request.user.username)
		return render(request,"your-timetable.html",{"user":user})
	else:
		return redirect('/teacher/login')

def forget(request):
	return render(request,'forget-password.html')

def forgot_mail(request):
	try:
		if request.method=='POST':
			user=teacherlogin.teach_obj.get(email=request.POST.get('email'))
		return index(request)
	except:
		messages.error(request, 'No user with this email found.')
		return forget(request)

def marks(request):
	from attendance.forms import mark_attendance_form
	return render(request,"marks.html",{"form":mark_attendance_form})

def studentlist(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():
		if request.method=='POST':
			curr_branch=branch_detail.branch_obj.get(name=request.POST.get('branch'),batch=request.POST.get('batch'),section=request.POST.get('section'))
			curr_subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
			student_list=list(studentlogin.stud_obj.filter(branch=curr_branch))
			curr_exam_type=request.POST.get('exam-type')
			for i in range(len(student_list)):
				try:
					student_list[i]=student_marks.marks_obj.get(semester=curr_branch.semester,student=student_list[i])
				except:
					student_list[i]=student_marks.marks_obj.create(student=student_list[i],branch=curr_branch,semester=curr_branch.semester,subject=curr_subject)
			return render(request,"studentlist.html",context={"student_list":student_list,"curr_branch":curr_branch,"curr_subject":curr_subject,'exam_type':curr_exam_type})
		else:
			return marks(request)
	else:
		return redirect('/teacher/login')

def mark_marks(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():
		if request.method=='POST':
			subject=subjects.sub_obj.get(subject_name=request.POST.get('subject'))
			branch=request.POST.get("branch")
			branch=User.objects.filter(groups__name=branch)
			exam_type=request.POST.get('exam-type')
			exam_type=exam_type.replace('-','')
			exam_type=exam_type.upper()
			print(dict(request.POST.items()))
			for i in branch:
				total_marks=0
				student=studentlogin.stud_obj.get(studentid=i)
				student_marks_obj=student_marks.marks_obj.get_or_create(student=student,subject=subject,branch=student.branch)[0]
				for ques in "1234567":
					for part in "abcdefghij":
						try:
							
							temp=int(request.POST.get(str(student)+'-'+ques+part))
							setattr(student_marks_obj,exam_type+'_Ques'+ques+'_part'+part.upper()+'_marks',temp)
							# print(temp)
						except Exception as e:
							# print(e)
							setattr(student_marks_obj,exam_type+'_Ques'+ques+'_part'+part.upper()+'_marks',0)
							
					try:
						temp2=int(request.POST.get(str(student)+'-'+ques))
					except Exception as e:
						print(e,2)
						temp2=0
					total_marks+=temp2
					setattr(student_marks_obj,exam_type+'_Ques'+ques+"_Marks",temp2)
				setattr(student_marks_obj,exam_type+"_total_marks",total_marks)
				student_marks_obj.save()

			return HttpResponseRedirect("/teacher/marks/")
		else:
			return marks(request)
	else:
		return redirect('/teacher/login')

def addPaper(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():
		subject_list=list(subjects.sub_obj.all())
		if request.method=="POST":
			subject=request.POST.get('subject')
			subject=subjects.sub_obj.get(subject_name=subject)

			ques_paper=question_paper()
			ques_paper.subject=subject
			ques_paper.semester=request.POST.get('semester')
			ques_paper.session=request.POST.get('session')
			total_sum=0
			for ques in "1234567":
				if 'marksques'+ques in request.POST:
					ques_marks_sum=int(request.POST.get('marksques'+ques))
				else:
					ques_marks_sum=0
				for part in 'ABCDEFGHIJ':
					try:
						temp=request.POST.get(ques+part.lower()+'.')
						setattr(ques_paper,"Ques"+ques+"_part"+part,temp)
						temp=int(request.POST.get(ques+part.lower()+'._marks'))
						setattr(ques_paper,"Ques"+ques+'_part'+part+"_marks",temp)
					except Exception as e:
						break
				setattr(ques_paper,"MarksQues"+ques,ques_marks_sum)
				total_sum+=ques_marks_sum
			setattr(ques_paper,"total_marks",total_sum)
			ques_paper.save()
			return HttpResponseRedirect("/teacher/marks")
			
		else:
			return render(request,'add-paper.html',{"subjects":subject_list})
	else:
		return redirect('/teacher/login')

def lds(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():
		teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
		subject_list=list(branch_subjects.branch_sub_obj.filter(subject_teacher=teacher))
		try:
			subject=request.GET.get('subject')
			branch=request.GET.get('branch')
			subject=subjects.sub_obj.get(subject_name=subject)
			teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
			subject_obj=branch_subjects.branch_sub_obj.get(subject_teacher=teacher,branch_subject=subject)
			executionData={}
			for i in range(1,76):
				try:
					lecture_detail=getattr(subject_obj,"lecture_"+str(i))
					# dateExec=dateExec["dateExecute"]
					if lecture_detail:
						print(lecture_detail,363)
						executionData[i]=lecture_detail
						print(executionData)
				except Exception as e:
					print(e)
				
			if subject and branch:
				return render(request,"ldsform.html",{'subject':subject,'branch':branch,"n":list(range(1,76)),"executionData":executionData})
		except Exception as e:
			pass
		return render(request,'lds.html',{"subject_list":subject_list})
	else:
		return redirect('/teacher/login')
	
def ldsform(request):
	if request.user.is_active and request.user.groups.filter(name="teacher").exists():
		if request.method=='POST':
			subject=request.POST.get('subject')
			subject=subjects.sub_obj.get(subject_name=subject)
			teacher=teacherlogin.teach_obj.get(teacherid=request.user.username)
			subject=branch_subjects.branch_sub_obj.get(subject_teacher=teacher,branch_subject=subject)
			for i in range(75):
				i=str(i)
				dateplan=request.POST.get('dateplan'+i)
				if not dateplan:
					continue
				dateplan=datetime.datetime.strptime(dateplan,"%Y-%m-%d").date().isoformat()
				
				unit=int(request.POST.get('unit'+i))
				topics=request.POST.getlist('topics'+i)
				data={
					"datePlan":dateplan,
					"dateExecute":dateplan,
					"unit":unit,
					"topics_planned":topics,
				}
				setattr(subject,"lecture_"+i,data)
				subject.save()
				print(getattr(subject,"lecture_"+i))
		return HttpResponseRedirect('/teacher/lds')
	else:
		return redirect('/teacher/login')

def load_topics(request):
    if request.user.is_active and request.user.groups.filter(name="teacher").exists():
        so=request.GET.get('unit')
        subject=request.GET.get('subject')
        print(subject,so)
        subject=subjects.sub_obj.get(subject_name=subject)
        topics_list=getattr(subject,"topics"+so)["topic_list"]
        
        return render(request,'load_topics.html',{"topics_list":topics_list})
    else:
        return redirect('/teacher/login')