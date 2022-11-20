from django.db import models
from django.core.validators import MinLengthValidator
from branch.models import branch_detail
from django.db.models.signals import post_save,post_delete
# from django.db import transaction
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from erp.settings import password,sender
from django.contrib.auth.models import User,Group
# Create your models here.

def createuser(**kwargs):
		fname=kwargs["instance"].student_name
		fname=fname.split()
		try:
			lname=fname[1]
		except:
			lname=''
		fname=fname[0]
		user = User.objects.create_user(username=kwargs["instance"].studentid,email=kwargs["instance"].email,password=kwargs["instance"].studentpwd,first_name=fname,last_name=lname)
		try:
			user_group = Group.objects.get(name='student')
		except:
			user_group=Group.objects.create(name="student")
		user.groups.add(user_group)
		branch_group=Group.objects.get(name=str(kwargs["instance"].branch))
		user.groups.add(branch_group)
def deleteuser(**kwargs):
	if isinstance(kwargs["instance"],studentlogin):
		try:
			u=User.objects.get(username=kwargs["instance"].studentid)
			u.delete()
		except Exception as e:
			print("******\n",e,"******\n")
class studentlogin(models.Model):
	studentid=models.CharField(max_length=20,primary_key=True)
	student_name=models.CharField(max_length=40)
	studentpwd=models.CharField(max_length=15,editable=False,validators=[
	MinLengthValidator(8, 'the field must contain at least 50 characters')
	])
	isactive=models.IntegerField(null=True)
	branch=models.ForeignKey(branch_detail,on_delete=models.CASCADE,related_name="branch",default=None)
	#branch=models.CharField(max_length=20)
	email=models.EmailField(max_length=60)

	def __str__(self):
		return self.studentid
	def mail(**kwargs):
		if  kwargs["created"] and isinstance(kwargs["instance"],studentlogin):
			
			alphabet = string.ascii_letters + string.digits + string.punctuation
			pwd=''
			for _ in range(10):
				pwd += ''.join(secrets.choice(alphabet))
			setattr(kwargs["instance"],'studentpwd',pwd)
			createuser(**kwargs)
			kwargs["instance"].save()

			receiver=kwargs["instance"].email
			user=kwargs["instance"].student_name
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
		elif isinstance(kwargs["instance"],studentlogin):
			u = User.objects.get(username=kwargs["instance"].studentid)
			u.set_password(kwargs["instance"].studentpwd)
			group=u.groups.all()
			for i in group:
				if str(i)=='student':
					continue 
				else:
					u.groups.remove(i)	
			branch_group=Group.objects.get(name=str(kwargs["instance"].branch))
			u.groups.add(branch_group)
			u.save()

	stud_obj = models.Manager()
	post_save.connect(mail)
	post_delete.connect(deleteuser)
	#transaction.on_commit(mail)
