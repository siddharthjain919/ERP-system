from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator

from erp.extra import MyLogger

logger=MyLogger(__name__).get_logger()
def create_branch_group(**kwargs):
	if kwargs["created"]  and isinstance(kwargs["instance"],branch_detail):
		branch=kwargs["instance"]
		g1 = Group.objects.create(name=str(branch))

def update_teacher_timetable(**kwargs):
	if isinstance(kwargs["instance"],branch_detail):
		branch=kwargs["instance"]
		print("Updating teacher timetable")
		for i in ['mon','tues','wed','thurs','fri','sat']:
			for j in range(1,9):
				lecture_name=i+'_lec'+str(j)
				#holds the new value
				lecture_details=getattr(branch,lecture_name)
				#holds the value stored in the database
				try:
					previous=getattr(branch_detail.branch_obj.get(name=branch.name,section=branch.section,batch=branch.batch),lecture_name)
				except Exception as e:
					previous=None
					
				if lecture_details:
					
					teacher_slot=getattr(lecture_details.subject_teacher,"teach_"+lecture_name)
					if teacher_slot and teacher_slot!=branch:
						raise Exception(f'{lecture_details.subject_teacher.name} already occupied at {lecture_name}!')
					if previous and previous!=lecture_details:
						logger.debug(f'Previous was {previous}, new input is {lecture_details}')
						setattr(previous.subject_teacher,"teach_"+lecture_name,None)
						previous.subject_teacher.save()
						print("Cleared",branch,"from",previous.subject_teacher,"at slot",lecture_name)
					setattr(lecture_details.subject_teacher,"teach_"+lecture_name,branch)
					lecture_details.subject_teacher.save()
				elif previous:
					print("cleared",branch,"from",previous.subject_teacher,"at slot",lecture_name)
					setattr(previous.subject_teacher,"teach_"+lecture_name,None)
					previous.subject_teacher.save()

def subject_check(**kwargs):
    if  isinstance(kwargs["instance"],branch_subjects):
        subject=kwargs["instance"]
        lecture_sum=subject.NOLR1+subject.NOLR2+subject.NOLR3+subject.NOLR4+subject.NOLR5
        if lecture_sum<40 and not subject.branch_subject.is_lab:
            raise Exception("Total lectures cannot be less than 40.")			

def delete_branch_group(**kwargs):
	if isinstance(kwargs['instance'],branch_detail):
		Group.objects.get(name=str(kwargs['instance'])).delete()

class branch_subjects(models.Model):
	branch=models.ForeignKey("branch.branch_detail",on_delete=models.CASCADE)
	branch_subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE,default=None)
	subject_teacher=models.ForeignKey("teacher.teacherlogin",on_delete=models.CASCADE,default=None)
	optional_teacher=models.ForeignKey("teacher.teacherlogin",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Teacher 2", related_name="optional_teacher")

	NOLR1=models.IntegerField(default=8)
	NOLT1=models.IntegerField(default=0,editable=False)

	NOLR2=models.IntegerField(default=8)
	NOLT2=models.IntegerField(default=0,editable=False)

	NOLR3=models.IntegerField(default=8)
	NOLT3=models.IntegerField(default=0,editable=False)

	NOLR4=models.IntegerField(default=8)
	NOLT4=models.IntegerField(default=0,editable=False)

	NOLR5=models.IntegerField(default=8)
	NOLT5=models.IntegerField(default=0,editable=False)
	
	for i in range(1,76):
		exec(f"lecture_{i}=models.JSONField(blank=True,null=True,editable=False)")
	
	def __str__(self):
		if self.optional_teacher:
			return self.branch_subject.subject_name+"-"+self.subject_teacher.name+'-'+self.optional_teacher.name
		return self.branch_subject.subject_name+"-"+self.subject_teacher.name	
	branch_sub_obj=models.Manager()
	class Meta:
		unique_together=[['branch_subject','subject_teacher','branch']]
	pre_save.connect(subject_check)

class branch_detail(models.Model):
	name=models.CharField(max_length=25)
	batch=models.IntegerField()
	course=models.ForeignKey("erp.course",on_delete=models.CASCADE)
	semester=models.IntegerField(default=1,validators=[MaxValueValidator(8),MinValueValidator(1)])
	section=models.CharField(max_length=1,help_text="Caps Only")

	total_strength=models.IntegerField(default=70)

	PSO_1=models.CharField(max_length=50)
	PSO_2=models.CharField(max_length=50)
	PSO_3=models.CharField(max_length=50)
	PSO_4=models.CharField(max_length=50)
	PSO_5=models.CharField(max_length=50)

	def __str__(self):
		return self.name+"("+self.section+")"+"-"+str(self.batch)
	branch_obj=models.Manager()

	class Meta:
		unique_together=[['name','batch','section']]

	mon_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l1',default=None,null=True,blank=True)
	mon_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l2',default=None,null=True,blank=True)
	mon_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l3',default=None,null=True,blank=True)
	mon_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l4',default=None,null=True,blank=True)
	mon_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l5',default=None,null=True,blank=True)
	mon_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l6',default=None,null=True,blank=True)
	mon_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l7',default=None,null=True,blank=True)
	mon_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='mon_l8',default=None,null=True,blank=True)

	tues_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l1',default=None,null=True,blank=True)
	tues_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l2',default=None,null=True,blank=True)
	tues_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l3',default=None,null=True,blank=True)
	tues_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l4',default=None,null=True,blank=True)
	tues_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l5',default=None,null=True,blank=True)
	tues_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l6',default=None,null=True,blank=True)
	tues_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l7',default=None,null=True,blank=True)
	tues_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='tues_l8',default=None,null=True,blank=True)

	wed_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l1',default=None,null=True,blank=True)
	wed_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l2',default=None,null=True,blank=True)
	wed_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l3',default=None,null=True,blank=True)
	wed_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l4',default=None,null=True,blank=True)
	wed_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l5',default=None,null=True,blank=True)
	wed_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l6',default=None,null=True,blank=True)
	wed_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l7',default=None,null=True,blank=True)
	wed_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='wed_l8',default=None,null=True,blank=True)

	thurs_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l1',default=None,null=True,blank=True)
	thurs_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l2',default=None,null=True,blank=True)
	thurs_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l3',default=None,null=True,blank=True)
	thurs_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l4',default=None,null=True,blank=True)
	thurs_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l5',default=None,null=True,blank=True)
	thurs_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l6',default=None,null=True,blank=True)
	thurs_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l7',default=None,null=True,blank=True)
	thurs_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='thurs_l8',default=None,null=True,blank=True)

	fri_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l1',default=None,null=True,blank=True)
	fri_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l2',default=None,null=True,blank=True)
	fri_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l3',default=None,null=True,blank=True)
	fri_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l4',default=None,null=True,blank=True)
	fri_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l5',default=None,null=True,blank=True)
	fri_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l6',default=None,null=True,blank=True)
	fri_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l7',default=None,null=True,blank=True)
	fri_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='fri_l8',default=None,null=True,blank=True)

	sat_lec1=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l1',default=None,null=True,blank=True)
	sat_lec2=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l2',default=None,null=True,blank=True)
	sat_lec3=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l3',default=None,null=True,blank=True)
	sat_lec4=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l4',default=None,null=True,blank=True)
	sat_lec5=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l5',default=None,null=True,blank=True)
	sat_lec6=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l6',default=None,null=True,blank=True)
	sat_lec7=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l7',default=None,null=True,blank=True)
	sat_lec8=models.ForeignKey(branch_subjects,on_delete=models.SET_NULL,related_name='sat_l8',default=None,null=True,blank=True)

	pre_save.connect(update_teacher_timetable)
	post_save.connect(create_branch_group)
	post_delete.connect(delete_branch_group)