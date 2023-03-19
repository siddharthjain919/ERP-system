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

from branch.models import branch_detail

def formatting(**kwargs):
	if isinstance(kwargs["instance"],studentlogin):
		student=kwargs["instance"]
		student.name=student.name.title()
		student.studentid=student.studentid.upper()

def createuser(**kwargs):
		fname=kwargs["instance"].name
		fname=fname.split()
		try:
			lname=fname[1]
		except:
			lname=''
		fname=fname[0]
		user = User.objects.create_user(username=kwargs["instance"].studentid,email=kwargs["instance"].personalEmail,password=kwargs["instance"].pwd,first_name=fname,last_name=lname)
		try:
			user_group = Group.objects.get(name='student')
		except:
			user_group=Group.objects.create(name="student")
		user.groups.add(user_group)
		branch_group=Group.objects.get(name=str(kwargs["instance"].branch))
		course_group=Group.objects.get(name=str(kwargs["instance"].branch.course))
		user.groups.add(course_group,branch_group)
		all_users=list(User.objects.filter(groups__name=branch_group))
		n=len(all_users)
		if n>=kwargs["instance"].branch.total_strength:
			batch1=Group.objects.get_or_create(name=str(kwargs["instance"].branch)+"_Batch1")[0]
			batch2=Group.objects.get_or_create(name=str(kwargs["instance"].branch)+"_Batch2")[0]

			for i in range(-(-n//2)):
				all_users[i].groups.add(batch1)
			for i in range(-(-n//2),n):
				all_users[i].groups.add(batch2)
			
			branch=kwargs["instance"].branch
			# batch1=branch_detail.branch_obj.get_or_create(name=str(branch)+"_Batch1",batch=branch.batch,course=branch.course,semester=branch.semester,)[0]



def deleteuser(**kwargs):
	if isinstance(kwargs["instance"],studentlogin):
		try:
			u=User.objects.get(username=kwargs["instance"].studentid)
			u.delete()
		except Exception as e:
			print("******\n",e,"******\n")
class studentlogin(models.Model):
	studentid=models.CharField(max_length=20,primary_key=True)
	name=models.CharField(max_length=40)
	gender=models.CharField(choices=(('MALE','MALE'),("FEMALE","FEMALE"),("OTHERS","OTHERS")),max_length=50)
	mobile=models.IntegerField(blank=True,null=True)
	DOB=models.DateField()
	DOA=models.DateField(default=timezone.now)
	pwd=models.CharField(max_length=15,editable=False,validators=[
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
	# bloodGroup=models.CharField(max_length=3,help_text="In Format A+")obile_Marks=models.IntegerField(null=True,blank=True)
	personalEmail=models.EmailField(max_length=50)
	# email=models.EmailField(max_length=60,editable=False,default=None)
	# maritalStatus=models.CharField(max_length=10,choices=(
	# 	("YES","YES"),
	# 	("NO","NO")
	# ))

	# fatherName=models.CharField(max_length=50)
	# father_mobile=models.IntegerField(null=True,blank=True)
	# fatherEmail=models.EmailField(max_length=30,null=True,blank=True)
	# fatherProfession=models.CharField(max_length=30)
	# father_income=models.IntegerField(null=True,blank=True)

	# motherName=models.CharField(max_length=50)
	# mother_mobile=models.IntegerField(null=True,blank=True)
	# motherEmail=models.EmailField(max_length=30,null=True,blank=True)
	# motherProfession=models.CharField(max_length=30)
	# mother_income=models.IntegerField(null=True,blank=True)

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
			setattr(kwargs["instance"],'pwd',pwd)
			createuser(**kwargs)
			kwargs["instance"].save()

		elif isinstance(kwargs["instance"],studentlogin):
			u = User.objects.get(username=kwargs["instance"].studentid)
			u.set_password(kwargs["instance"].pwd)
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


	#for st1
	ST1_Ques1_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partC_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partD_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partE_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partF_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partG_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partH_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partI_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques1_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_partC_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_partD_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_partE_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques2_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques3_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques3_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques3_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques4_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques4_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques4_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques5_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques5_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques5_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques6_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques6_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques6_Marks=models.IntegerField(null=True,blank=True)
	ST1_Ques7_partA_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques7_partB_marks=models.IntegerField(null=True,blank=True)
	ST1_Ques7_Marks=models.IntegerField(null=True,blank=True)

	ST1_total_marks=models.IntegerField(null=True,blank=True)


	# for st-2

	ST2_Ques1_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partC_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partD_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partE_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partF_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partG_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partH_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partI_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques1_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_partC_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_partD_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_partE_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques2_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques3_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques3_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques3_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques4_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques4_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques4_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques5_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques5_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques5_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques6_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques6_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques6_Marks=models.IntegerField(null=True,blank=True)
	ST2_Ques7_partA_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques7_partB_marks=models.IntegerField(null=True,blank=True)
	ST2_Ques7_Marks=models.IntegerField(null=True,blank=True)

	ST2_total_marks=models.IntegerField(null=True,blank=True)

	# REST

	REST_Ques1_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partC_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partD_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partE_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partF_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partG_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partH_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partI_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
	REST_Ques1_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_partC_marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_partD_marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_partE_marks=models.IntegerField(null=True,blank=True)
	REST_Ques2_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques3_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques3_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques3_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques4_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques4_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques4_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques5_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques5_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques5_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques6_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques6_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques6_Marks=models.IntegerField(null=True,blank=True)
	REST_Ques7_partA_marks=models.IntegerField(null=True,blank=True)
	REST_Ques7_partB_marks=models.IntegerField(null=True,blank=True)
	REST_Ques7_Marks=models.IntegerField(null=True,blank=True)

	REST_total_marks=models.IntegerField(null=True,blank=True)


	# PUE


	PUE_Ques1_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partC_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partD_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partE_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partF_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partG_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partH_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partI_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques1_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_partC_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_partD_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_partE_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques2_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques3_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques3_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques3_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques4_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques4_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques4_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques5_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques5_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques5_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques6_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques6_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques6_Marks=models.IntegerField(null=True,blank=True)
	PUE_Ques7_partA_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques7_partB_marks=models.IntegerField(null=True,blank=True)
	PUE_Ques7_Marks=models.IntegerField(null=True,blank=True)

	PUE_total_marks=models.IntegerField(null=True,blank=True)


	# REPUE


	REPUE_Ques1_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partC_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partD_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partE_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partF_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partG_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partH_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partI_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques1_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_partC_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_partD_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_partE_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques2_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques3_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques3_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques3_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques4_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques4_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques4_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques5_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques5_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques5_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques6_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques6_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques6_Marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques7_partA_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques7_partB_marks=models.IntegerField(null=True,blank=True)
	REPUE_Ques7_Marks=models.IntegerField(null=True,blank=True)

	REPUE_total_marks=models.IntegerField(null=True,blank=True)







	marks_obj=models.Manager()
	def __str__(self) -> str:
		return str(self.student)+"||"+str(self.branch)+"||"+str(self.subject)

