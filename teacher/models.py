from django.db import models
from django.core.validators import MinLengthValidator
from branch.models import branch_detail
from django.db.models.signals import post_save
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your models here.
class teacherlogin(models.Model):
	teacherid=models.CharField(max_length=20,primary_key=True)
	Name=models.CharField(max_length=40)
	teacherpwd=models.CharField(max_length=15,editable=False,validators=[MinLengthValidator(8, 'the field must contain at least 8 characters')])
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
