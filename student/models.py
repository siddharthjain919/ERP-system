from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save,post_delete,pre_save
from django.utils import timezone
# from django.db import transaction
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from erp.settings import password,sender
from django.contrib.auth.models import User,Group
# Create your models here.
from datetime import date

def formatting(**kwargs):
	if isinstance(kwargs["instance"],studentlogin):
		student=kwargs["instance"]
		student.student_name=student.student_name.title()
		student.studentid=student.studentid.upper()

def createuser(**kwargs):
		fname=kwargs["instance"].student_name
		fname=fname.split()
		try:
			lname=fname[1]
		except:
			lname=''
		fname=fname[0]
		user = User.objects.create_user(username=kwargs["instance"].studentid,email=kwargs["instance"].personalEmail,password=kwargs["instance"].studentpwd,first_name=fname,last_name=lname)
		try:
			user_group = Group.objects.get(name='student')
		except:
			user_group=Group.objects.create(name="student")
		user.groups.add(user_group)
		branch_group=Group.objects.get(name=str(kwargs["instance"].branch))
		course_group=Group.objects.get(name=str(kwargs["instance"].branch.course))
		user.groups.add(course_group,branch_group)
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
	gender=models.CharField(choices=(('MALE','MALE'),("FEMALE","FEMALE"),("OTHERS","OTHERS")),max_length=50)
	DOB=models.DateField()
	DOA=models.DateField(default=timezone.now)
	studentpwd=models.CharField(max_length=15,editable=False,validators=[
	MinLengthValidator(8, 'the field must contain at least 50 characters')
	])
	course=models.ForeignKey("erp.course",on_delete=models.CASCADE)
	branch=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE,related_name="branch",default=None)
	# semester=models.IntegerField(default=1,validators=[MaxValueValidator(8),MinValueValidator(1)])
	# category=models.CharField(max_length=50,choices=(
	# 	("GEN","GEN"),
	# 	("OBC","OBC"),
	# 	("SC","SC"),
	# 	("ST","ST"),
	# 	("OTHERS","OTHERS")
	# ))
	# religion=models.CharField(max_length=50)
	# admissionThrough=models.CharField(max_length=50,choices=(
	# 	("DIRECT","DIRECT"),
	# 	("COUNSELLING","COUNSELLING")
	# ))
	# admissionUnder=models.CharField(max_length=30) #change
	# status=models.CharField(max_length=30) #change
	# sub_status=models.CharField(max_length=30) #change
	# bloodGroup=models.CharField(max_length=3,help_text="In Format A+")
	# mobile=models.IntegerField()
	personalEmail=models.EmailField(max_length=30)
	# email=models.EmailField(max_length=60,editable=False,default=None)
	# maritalStatus=models.CharField(max_length=10,choices=(
	# 	("YES","YES"),
	# 	("NO","NO")
	# ))

	# fatherName=models.CharField(max_length=50)
	# fatherMobile=models.IntegerField()
	# fatherEmail=models.EmailField(max_length=30,null=True,blank=True)
	# fatherProfession=models.CharField(max_length=30)
	# fatherIncome=models.IntegerField()

	# motherName=models.CharField(max_length=50)
	# motherMobile=models.IntegerField()
	# motherEmail=models.EmailField(max_length=30,null=True,blank=True)
	# motherProfession=models.CharField(max_length=30)
	# motherIncome=models.IntegerField()

	# permanentAddress=models.CharField(max_length=100)
	# currAddress=models.CharField(max_length=100)
	# session=models.IntegerField(validators=[MaxValueValidator(int(date.today().year))],default=int(date.today().year))

	# adhar=models.IntegerField(validators=[MinValueValidator(100000000000),MaxValueValidator(999999999999)],verbose_name="Adhar")
	
	# highSchoolRollNo=models.IntegerField(verbose_name="10th Roll Number")
	# highSchoolName=models.CharField(max_length=30,verbose_name="10th School Name")
	# highSchoolBoard=models.CharField(max_length=30,verbose_name="10th Board",help_text="In Format CBSE/UP")
	# highSchoolPassingYear=models.IntegerField(verbose_name="10th Passing Year",validators=[MaxValueValidator(int(date.today().year)-2)],default=int(date.today().year)-2)
	# highSchoolMarks=models.IntegerField(verbose_name="10th Total Marks")
	# highSchoolPercentage=models.FloatField(verbose_name="10th percentage")

	# IntermediateRollNo=models.IntegerField(verbose_name="12th Roll Number")
	# IntermediateName=models.CharField(max_length=30,verbose_name="12th School Name")
	# IntermediateBoard=models.CharField(max_length=30,verbose_name="12th Board",help_text="In Format CBSE/UP")
	# IntermediatePassingYear=models.IntegerField(verbose_name="12th Passing Year",validators=[MaxValueValidator(int(date.today().year)-2)],default=int(date.today().year)-2)
	# IntermediateMarks=models.IntegerField(verbose_name="12th Total Marks")
	# IntermediatePercentage=models.FloatField(verbose_name="12th percentage")
	# PCMpercentage=models.FloatField(verbose_name="PCM Percentage")

	# hosteller=models.BooleanField()
	# hostelName=models.CharField(verbose_name="Hostel Name",max_length=20,blank=True,null=True)

	def __str__(self):
		return self.studentid
	def mail(**kwargs):
		if  kwargs["created"] and isinstance(kwargs["instance"],studentlogin):
			
			alphabet = string.ascii_letters + string.digits + string.punctuation
			pwd=''
			for _ in range(8):
				pwd += ''.join(secrets.choice(alphabet))
			setattr(kwargs["instance"],'studentpwd',pwd)
			createuser(**kwargs)
			kwargs["instance"].save()

			receiver=kwargs["instance"].personalEmail
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
	pre_save.connect(formatting)
	post_save.connect(mail)
	post_delete.connect(deleteuser)

	#transaction.on_commit(mail)

class student_marks(models.Model):
	student=models.ForeignKey(studentlogin,on_delete=models.CASCADE)
	subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE)
	semester=models.IntegerField(blank=True,null=True)
	branch=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE)
	assignment1_marks=models.IntegerField(blank=True,null=True)
	assignment2_marks=models.IntegerField(blank=True,null=True)
	assignment3_marks=models.IntegerField(blank=True,null=True)
	assignment4_marks=models.IntegerField(blank=True,null=True)
	assignment5_marks=models.IntegerField(blank=True,null=True)
	st1_marks=models.IntegerField(blank=True,null=True)
	st2_marks=models.IntegerField(blank=True,null=True)
	pue_marks=models.IntegerField(blank=True,null=True)
	re_pue_marks=models.IntegerField(blank=True,null=True)

	marks_obj=models.Manager()
	def __str__(self) -> str:
		return str(self.student)+"||"+str(self.branch)+"||"+str(self.subject)

