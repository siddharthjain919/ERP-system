from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from .models import teacherlogin
from branch.models import branch_subjects,branch_detail
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from erp.models import subjects
branch=None
def index(request):
	return render(request,'login.html')
def login(request):
	if request.method == 'POST':
		username = request.POST.get('teacherid')
		password = request.POST.get('teacherpwd')
		try:
			user = teacherlogin.teach_obj.get(teacherid=username,teacherpwd=password)
			print(user)
			user2 = authenticate(request, username=username, password=password)
			if user is not None:
				auth_login(request,user2)
				return render(request, 'dash1.html', {})
			else:
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username,password))
				return redirect('/')
		except Exception as identifier:
			print(111111111111111111111111,identifier)
			return redirect('/teacher')
	else:
		return render(request,'login.html')
def coordinatorlogin(request):
	if request.method == 'POST':
		username = request.POST.get('teacherid')
		password = request.POST.get('teacherpwd')
		try:
			user = teacherlogin.teach_obj.get(teacherid=username,teacherpwd=password)
			user2 = authenticate(request, username=username, password=password)
			print(user,user2,username,password)
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
@login_required(login_url='/teacher/login/')
def timetable(request):
	print(request.user,22222222222222)
	if not request.user.is_authenticated:
		return redirect('/teacher')
	if branch:
		timetable_list=branch_detail.branch_obj.get(pk=branch)
		subject_list=list(branch_subjects.branch_sub_obj.all())
		return render(request,'timetable.html',context={'timetable_list':timetable_list,"subject_list":subject_list})
	else:
		return render(request,'login.html')
@login_required(login_url='/teacher/login/')
def update(request):
	global branch
	ob=branch_detail.branch_obj.get(pk=branch)
	print(ob,type(ob))
	if request.method=='POST':
		for i in ['mon','tues','wed','thurs','fri','sat']:
			for j in range(1,9):
				temp=i+'_lec'+str(j)
				temp2=request.POST.get(temp)
				
				pass
				#messages.success(request,"Timetable Updated")
	print("****Success****")
	return timetable(request)
@login_required(login_url='/teacher/login/')
def subject(request):
	global branch
	subject_list=list(subjects.sub_obj.all().values_list('subject_name'))
	return render(request,'subjects.html',context={'subject_list':subject_list,'n':range(len(subject_list))})
@login_required(login_url='/teacher/login/')
def add(request):
	subject_list=list(subjects.sub_obj.all().values_list('subject'))
	code=request.POST.get('code').upper()
	code=code.replace('-','')
	name=request.POST.get('name').title()
	code=''.join(code.split())
	code=code[:3]+' '+code[3:]
	code=code+': '+name
	name=(code,)
	if name not in subject_list:
		ob=subjects.sub_obj.create(subject=code)
	else:
		pass
	return subject(request)
@login_required(login_url='/teacher/login/')
def attendance(request):
	return render(request,"attendance.html",{})
