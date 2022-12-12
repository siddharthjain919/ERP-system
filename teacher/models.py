from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail
from django.db.models.signals import post_save,post_delete
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from erp.settings import password,sender
# Create your models here.
def createuser(**kwargs):
		fname=kwargs["instance"].Name
		fname=fname.split()
		try:
			lname=fname[1]
		except:
			lname=''
		fname=fname[0]
		user = User.objects.create_user(username=kwargs["instance"].teacherid,email=kwargs["instance"].email,password=kwargs["instance"].teacherpwd,first_name=fname,last_name=lname)
		try:
			user_group = Group.objects.get(name='teacher')
		except:
			user_group=Group.objects.create(name="teacher")
		user.groups.add(user_group)
		user.is_staff=True
		user.save()
def deleteuser(**kwargs):
	if isinstance(kwargs["instance"],teacherlogin):
		try:
			u=User.objects.get(username=kwargs["instance"].teacherid)
			u.delete()
		except Exception as e:
			print("from line 30 in teacher models")
			print("******\n",e,"\n******")
class teacherlogin(models.Model):

	teacherid=models.CharField(max_length=20,primary_key=True)
	Name=models.CharField(max_length=40)
	teacherpwd=models.CharField(max_length=15,validators=[MinLengthValidator(8, 'the field must contain at least 8 characters')])
	isactive=models.IntegerField(null=True,blank=True)
	cc_of_branch=models.ForeignKey("branch.branch_detail",null=True,blank=True,default=None,on_delete=models.CASCADE)
	email=models.EmailField(max_length=50)

	teach_mon_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l1',default=None,null=True,editable=False)
	teach_mon_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l2',default=None,null=True,editable=False)
	teach_mon_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l3',default=None,null=True,editable=False)
	teach_mon_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l4',default=None,null=True,editable=False)
	teach_mon_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l5',default=None,null=True,editable=False)
	teach_mon_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l6',default=None,null=True,editable=False)
	teach_mon_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l7',default=None,null=True,editable=False)
	teach_mon_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_mon_l8',default=None,null=True,editable=False)

	teach_tues_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l1',default=None,null=True,editable=False)
	teach_tues_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l2',default=None,null=True,editable=False)
	teach_tues_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l3',default=None,null=True,editable=False)
	teach_tues_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l4',default=None,null=True,editable=False)
	teach_tues_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l5',default=None,null=True,editable=False)
	teach_tues_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l6',default=None,null=True,editable=False)
	teach_tues_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l7',default=None,null=True,editable=False)
	teach_tues_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_tues_l8',default=None,null=True,editable=False)

	teach_wed_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l1',default=None,null=True,editable=False)
	teach_wed_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l2',default=None,null=True,editable=False)
	teach_wed_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l3',default=None,null=True,editable=False)
	teach_wed_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l4',default=None,null=True,editable=False)
	teach_wed_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l5',default=None,null=True,editable=False)
	teach_wed_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l6',default=None,null=True,editable=False)
	teach_wed_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l7',default=None,null=True,editable=False)
	teach_wed_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_wed_l8',default=None,null=True,editable=False)

	teach_thurs_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l1',default=None,null=True,editable=False)
	teach_thurs_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l2',default=None,null=True,editable=False)
	teach_thurs_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l3',default=None,null=True,editable=False)
	teach_thurs_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l4',default=None,null=True,editable=False)
	teach_thurs_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l5',default=None,null=True,editable=False)
	teach_thurs_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l6',default=None,null=True,editable=False)
	teach_thurs_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l7',default=None,null=True,editable=False)
	teach_thurs_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_thurs_l8',default=None,null=True,editable=False)

	teach_fri_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l1',default=None,null=True,editable=False)
	teach_fri_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l2',default=None,null=True,editable=False)
	teach_fri_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l3',default=None,null=True,editable=False)
	teach_fri_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l4',default=None,null=True,editable=False)
	teach_fri_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l5',default=None,null=True,editable=False)
	teach_fri_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l6',default=None,null=True,editable=False)
	teach_fri_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l7',default=None,null=True,editable=False)
	teach_fri_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_fri_l8',default=None,null=True,editable=False)

	teach_sat_lec1=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l1',default=None,null=True,editable=False)
	teach_sat_lec2=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l2',default=None,null=True,editable=False)
	teach_sat_lec3=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l3',default=None,null=True,editable=False)
	teach_sat_lec4=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l4',default=None,null=True,editable=False)
	teach_sat_lec5=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l5',default=None,null=True,editable=False)
	teach_sat_lec6=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l6',default=None,null=True,editable=False)
	teach_sat_lec7=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l7',default=None,null=True,editable=False)
	teach_sat_lec8=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name='teach_sat_l8',default=None,null=True,editable=False)

	teach_obj = models.Manager()
	def __str__(self):
		return self.teacherid
	
	def mail(**kwargs):
		if kwargs["created"] and isinstance(kwargs["instance"],teacherlogin):
			letters = string.ascii_letters
			digits = string.digits
			special_chars = string.punctuation
			alphabet = letters + digits + special_chars
			pwd=''
			for _ in range(8):
				pwd += ''.join(secrets.choice(alphabet))
			setattr(kwargs["instance"],'teacherpwd',pwd)
			

			#for adding user to group
			createuser(**kwargs)
			kwargs["instance"].save()
			#sending mails
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
			except Exception as e:
				print("from line 132 in teacher models")
				print("******\n",e,"\n******")
		elif isinstance(kwargs["instance"],teacherlogin):
			u = User.objects.get(username=kwargs["instance"].teacherid)
			u.set_password(kwargs["instance"].teacherpwd)
			u.save()

	post_save.connect(mail)
	post_delete.connect(deleteuser)

