from django.db import models
from django.core.validators import MinLengthValidator
from branch.models import branch_detail
from django.db.models.signals import post_save
import smtplib,secrets,string
import win32com.client as win32

# Create your models here.
class teacherlogin(models.Model):
	teacherid=models.CharField(max_length=20)
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

			olApp=win32.Dispatch("Outlook.Application")
			olNS=olApps.GetNameSpace('MAPI')
			mail_item=olApps.CreateItem(0)
			mail_item.Subject='Text Mail'
			mail_item.Body='Hi, How arr you?'
			mail_item.To='abhinavsinghal256@gmail.com'
			mail_item.Sender='abhinav.19b111050@abes.ac.in'
			mail_item._oleobj_.Invoke(*(64209,8,0,olNS.Accounts.Item('abhinav.19b111050@abes.ac.in')))
			mail_item.Display()
			mail_item.Save()
			mail_item.Send()
			'''
			send_mail(
			    'Subject here',
			    'Here is the message.',
			    'abhinav.19b111050@abes.ac.in',
			    ['abhinavsinghal256@gmail.com'],
			    fail_silently=False,
				auth_user="abhinav.19b111050@abes.ac.in",
				auth_password="Abhi.abes",

			)'''

	post_save.connect(mail)
