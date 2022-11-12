from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from branch.models import branch_detail, branch_subjects
from erp.models import subjects

from .models import teacherlogin

branch=None
def index(request):
	return render(request,'login.html')
def login(request):
	if request.method == 'POST':
		username = request.POST.get('teacherid')
		password = request.POST.get('teacherpwd')
		try:
			user = teacherlogin.teach_obj.get(teacherid=username,teacherpwd=password)
			# print(user)
			user2 = authenticate(request, username=username, password=password)
			if user is not None:
				auth_login(request,user2)
				return render(request, 'dash1.html', {})
			else:
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username,password))
				return redirect('/')
		except Exception as identifier:
			print("******\n",identifier,"******\n")
			return redirect('/teacher')
	elif request.user.is_authenticated:
		return render(request, 'dash1.html', {})
	else:
		return render(request,'login.html')
def coordinatorlogin(request):
	if request.method == 'POST':
		username = request.POST.get('teacherid')
		password = request.POST.get('teacherpwd')
		try:
			user = teacherlogin.teach_obj.get(teacherid=username,teacherpwd=password)
			user2 = authenticate(request, username=username, password=password)
			if user is not None:
				global branch
				auth_login(request,user2)
				branch=teacherlogin.teach_obj.filter(teacherid=user)
				branch=branch[0].cc_of_branch
				if not branch:
					return redirect('/teacher')
				return render(request, 'dash1.html', {})
			else:
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username,password))
				return redirect('/')
		except Exception as identifier:
			return redirect('/teacher')
	else:
		return render(request,'login.html')

def logout(request):
	request.session.flush()
	auth_logout(request)
	return redirect('/teacher')
def timetable(request):
	
	branch_list=list(branch_detail.branch_obj.all())
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	if branch:
		# print(branch)
		subject_list=list(branch_subjects.branch_sub_obj.all())
		return render(request,'timetable.html',context={"branch_list":branch_list,"subject_list":subject_list})
	else:
		return render(request,'timetable.html',context={"branch_list":branch_list})

def update(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	#print(branch,type(branch))
	if request.method=='POST':
		branch=request.POST.get("branch")
		branch=branch_detail.branch_obj.get(name=branch)
		for i in ['mon','tues','wed','thurs','fri','sat']:
			for j in range(1,9):
				lecture_name=i+'_lec'+str(j)
				lecture_input=request.POST.get(lecture_name)
				# print(1,lecture_input,type(lecture_input))
				previous=getattr(branch,lecture_name)
				##print(lecture_input,previous)
				# print(2,previous,type(previous))
				# print(lecture_input,previous,type(lecture_input),11111111111111)
				if lecture_input=='':
					continue
				if lecture_input:
					lecture_input=lecture_input.split('-')
					subject_name=lecture_input[0]
					subject_name=subjects.sub_obj.get(subject_name=subject_name)
					subject_teacher=lecture_input[1]
					subject_teacher=teacherlogin.teach_obj.get(Name=subject_teacher)
					teacher_slot=getattr(subject_teacher,"teach_"+lecture_name)
					if teacher_slot and teacher_slot!=branch:
						raise Exception(subject_teacher.Name,"already occupied at",lecture_name)
					if previous and lecture_input!=previous:
						setattr(previous.subject_teacher,"teach_"+lecture_name,None)
						previous.subject_teacher.save()
					setattr(subject_teacher,"teach_"+lecture_name,branch)
					
					subject_teacher.save()
					setattr(branch,lecture_name,branch_subjects.branch_sub_obj.get(subject_teacher=subject_teacher,branch_subject=subject_name))
					# print(1,subject_name,type(subject_name))
					# print(2,subject_teacher,type(subject_teacher))
				elif previous:
					setattr(previous.subject_teacher,"teach_"+lecture_name,None)
					previous.subject_teacher.save()
					setattr(branch,lecture_name,None)
				else:
					setattr(branch,lecture_name,None)
				branch.save()
				
				#messages.success(request,"Timetable Updated")
	print("****Success****")
	print(request.user,request.user.is_authenticated)
	return timetable(request)

def subject(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	global branch
	subject_list=list(branch_subjects.branch_sub_obj.all())
	all_subjects=list(subjects.sub_obj.all())
	teacher_list=list(teacherlogin.teach_obj.all())
	for i in range(len(subject_list)):
		subject_list[i]=str(subject_list[i])
		subject_list[i]=subject_list[i].split('-')
	return render(request,'subjects.html',context={'branch_subject':subject_list,"all_subjects":all_subjects,"teacher_list":teacher_list})

def add(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	subject_list=list(branch_subjects.branch_sub_obj.all())
	name=request.POST.get('subject_name')
	name=subjects.sub_obj.get(subject_name=name)
	faculty=request.POST.get("subject_teacher")
	faculty=teacherlogin.teach_obj.get(Name=faculty)
	for sub in subject_list:
		if sub.branch_subject==name and sub.subject_teacher==faculty:
			break 
	else:
		ob=branch_subjects.branch_sub_obj.create(branch_subject=name,subject_teacher=faculty)
	return subject(request)

def attendance(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	return render(request,"attendance.html",{})

def about(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	return render(request,"about.html",{})

def teachertimetable(request):
	if not request.user.is_authenticated:
		return redirect('/teacher/login')
	user = teacherlogin.teach_obj.get(teacherid=request.user.username)
	return render(request,"your-timetable.html",{"user":user})