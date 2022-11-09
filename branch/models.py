from django.db import models
from django.db.models.signals import pre_save
from teacher.models import teacherlogin
# Create your models here.

def update_teacher_timetable(**kwargs):
	if isinstance(kwargs["instance"],branch_detail):
		branch=kwargs["instance"]
		print(branch,type(branch.mon_lec1),branch_detail.branch_obj.get(name=branch.name).mon_lec1)
		for i in ['mon','tues','wed','thurs','fri','sat']:
			for j in range(1,9):
				lecture_name=i+'_lec'+str(j)
				#holds the new value
				lecture_details=getattr(branch,lecture_name)
				#holds the value stored in the database
				previous=getattr(branch_detail.branch_obj.get(name=branch.name),lecture_name)
				if lecture_details:
					teacher_slot=getattr(lecture_details.subject_teacher,"teach_"+lecture_name)
					if teacher_slot and teacher_slot!=branch:
						raise Exception(lecture_details.subject_teacher.Name,"already occupied at",lecture_name)
					if previous!=lecture_details:
						setattr(previous.subject_teacher,"teach_"+lecture_name,None)
						previous.subject_teacher.save()
						print("cleared",branch,"from",previous.subject_teacher,"at slot",lecture_name)
					setattr(lecture_details.subject_teacher,"teach_"+lecture_name,branch)
					lecture_details.subject_teacher.save()
				elif previous:
					setattr(previous.subject_teacher,"teach_"+lecture_name,None)
					previous.subject_teacher.save()
					
class branch_subjects(models.Model):
	branch_subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE,default=None)
	subject_teacher=models.ForeignKey("teacher.teacherlogin",on_delete=models.CASCADE,default=None)
	def __str__(self):
		return self.branch_subject.subject_name+"-"+self.subject_teacher.Name	
	branch_sub_obj=models.Manager()
	class Meta:
		unique_together=[['branch_subject','subject_teacher']]
class branch_detail(models.Model):
	name=models.CharField(max_length=25,primary_key=True)
	batch=models.IntegerField()
	def __str__(self):
		return self.name
	branch_obj=models.Manager()
	mon_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l1',default=None,null=True,blank=True)
	mon_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l2',default=None,null=True,blank=True)
	mon_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l3',default=None,null=True,blank=True)
	mon_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l4',default=None,null=True,blank=True)
	mon_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l5',default=None,null=True,blank=True)
	mon_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l6',default=None,null=True,blank=True)
	mon_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l7',default=None,null=True,blank=True)
	mon_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l8',default=None,null=True,blank=True)

	tues_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l1',default=None,null=True,blank=True)
	tues_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l2',default=None,null=True,blank=True)
	tues_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l3',default=None,null=True,blank=True)
	tues_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l4',default=None,null=True,blank=True)
	tues_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l5',default=None,null=True,blank=True)
	tues_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l6',default=None,null=True,blank=True)
	tues_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l7',default=None,null=True,blank=True)
	tues_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l8',default=None,null=True,blank=True)

	wed_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l1',default=None,null=True,blank=True)
	wed_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l2',default=None,null=True,blank=True)
	wed_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l3',default=None,null=True,blank=True)
	wed_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l4',default=None,null=True,blank=True)
	wed_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l5',default=None,null=True,blank=True)
	wed_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l6',default=None,null=True,blank=True)
	wed_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l7',default=None,null=True,blank=True)
	wed_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l8',default=None,null=True,blank=True)

	thurs_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l1',default=None,null=True,blank=True)
	thurs_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l2',default=None,null=True,blank=True)
	thurs_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l3',default=None,null=True,blank=True)
	thurs_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l4',default=None,null=True,blank=True)
	thurs_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l5',default=None,null=True,blank=True)
	thurs_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l6',default=None,null=True,blank=True)
	thurs_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l7',default=None,null=True,blank=True)
	thurs_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l8',default=None,null=True,blank=True)

	fri_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l1',default=None,null=True,blank=True)
	fri_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l2',default=None,null=True,blank=True)
	fri_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l3',default=None,null=True,blank=True)
	fri_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l4',default=None,null=True,blank=True)
	fri_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l5',default=None,null=True,blank=True)
	fri_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l6',default=None,null=True,blank=True)
	fri_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l7',default=None,null=True,blank=True)
	fri_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l8',default=None,null=True,blank=True)

	sat_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l1',default=None,null=True,blank=True)
	sat_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l2',default=None,null=True,blank=True)
	sat_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l3',default=None,null=True,blank=True)
	sat_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l4',default=None,null=True,blank=True)
	sat_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l5',default=None,null=True,blank=True)
	sat_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l6',default=None,null=True,blank=True)
	sat_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l7',default=None,null=True,blank=True)
	sat_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l8',default=None,null=True,blank=True)

	pre_save.connect(update_teacher_timetable)