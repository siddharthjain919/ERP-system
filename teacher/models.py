from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator
from branch.models import branch_detail
from django.db.models.signals import post_save
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
# Create your models here.
class teacherlogin(models.Model):
	teacherid=models.CharField(max_length=20,primary_key=True)
	Name=models.CharField(max_length=40)
	teacherpwd=models.CharField(max_length=15,validators=[MinLengthValidator(8, 'the field must contain at least 8 characters')])
	isactive=models.IntegerField(null=True,blank=True)
	cc_of_branch=models.ForeignKey(branch_detail,null=True,blank=True,default=None,on_delete=models.CASCADE)
	email=models.EmailField(max_length=50)
	def __str__(self):
		return self.teacherid
	teach_obj = models.Manager()
	def mail(**kwargs):
		if kwargs["created"] and isinstance(kwargs["instance"],teacherlogin):
			letters = string.ascii_letters
			digits = string.digits
			special_chars = string.punctuation
			alphabet = letters + digits + special_chars

			pwd=''
			for _ in range(10):
				pwd += ''.join(secrets.choice(alphabet))
			setattr(kwargs["instance"],'teacherpwd',pwd)
			kwargs["instance"].save()

			#for adding user to group
			fname=kwargs["instance"].Name
			fname=fname.split()
			try:
				lname=fname[1]
			except:
				lname=''
			fname=fname[0]
			user = User.objects.create_user(username=kwargs["instance"].teacherid,email=kwargs["instance"].email,password=pwd,first_name=fname,last_name=lname)
			user_group = Group.objects.get(name='teacher')
			user.groups.add(user_group)

			#sending mails
			password="oqmdkyfhgkxeolfk"
			sender="abhinavsinghal256@gmail.com"
			receiver=kwargs["instance"].email
			user=kwargs["instance"].Name
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
				print("error")

	post_save.connect(mail)

class teacher_timetable(teacherlogin):
	mon_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l1',default=None,null=True)
	mon_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l2',default=None,null=True)
	mon_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l3',default=None,null=True)
	mon_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l4',default=None,null=True)
	mon_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l5',default=None,null=True)
	mon_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l6',default=None,null=True)
	mon_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l7',default=None,null=True)
	mon_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='mon_l8',default=None,null=True)

	tues_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l1',default=None,null=True)
	tues_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l2',default=None,null=True)
	tues_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l3',default=None,null=True)
	tues_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l4',default=None,null=True)
	tues_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l5',default=None,null=True)
	tues_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l6',default=None,null=True)
	tues_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l7',default=None,null=True)
	tues_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='tues_l8',default=None,null=True)

	wed_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l1',default=None,null=True)
	wed_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l2',default=None,null=True)
	wed_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l3',default=None,null=True)
	wed_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l4',default=None,null=True)
	wed_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l5',default=None,null=True)
	wed_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l6',default=None,null=True)
	wed_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l7',default=None,null=True)
	wed_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='wed_l8',default=None,null=True)

	thurs_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l1',default=None,null=True)
	thurs_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l2',default=None,null=True)
	thurs_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l3',default=None,null=True)
	thurs_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l4',default=None,null=True)
	thurs_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l5',default=None,null=True)
	thurs_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l6',default=None,null=True)
	thurs_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l7',default=None,null=True)
	thurs_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='thurs_l8',default=None,null=True)

	fri_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l1',default=None,null=True)
	fri_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l2',default=None,null=True)
	fri_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l3',default=None,null=True)
	fri_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l4',default=None,null=True)
	fri_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l5',default=None,null=True)
	fri_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l6',default=None,null=True)
	fri_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l7',default=None,null=True)
	fri_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='fri_l8',default=None,null=True)

	sat_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l1',default=None,null=True)
	sat_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l2',default=None,null=True)
	sat_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l3',default=None,null=True)
	sat_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l4',default=None,null=True)
	sat_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l5',default=None,null=True)
	sat_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l6',default=None,null=True)
	sat_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l7',default=None,null=True)
	sat_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='sat_l8',default=None,null=True)
