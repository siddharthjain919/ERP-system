from dataclasses import Field
from django.db import models
# Create your models here.

class branch_subjects(models.Model):
	branch_subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE,default=None)
	
class branch_detail(models.Model):

	name=models.CharField(max_length=25,primary_key=True)
	batch=models.IntegerField()
	def __str__(self):
	    return self.name
	branch_obj=models.Manager()
	mon_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l1',default=None,null=True)
	mon_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l2',default=None,null=True)
	mon_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l3',default=None,null=True)
	mon_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l4',default=None,null=True)
	mon_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l5',default=None,null=True)
	mon_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l6',default=None,null=True)
	mon_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l7',default=None,null=True)
	mon_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='mon_l8',default=None,null=True)

	tues_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l1',default=None,null=True)
	tues_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l2',default=None,null=True)
	tues_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l3',default=None,null=True)
	tues_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l4',default=None,null=True)
	tues_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l5',default=None,null=True)
	tues_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l6',default=None,null=True)
	tues_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l7',default=None,null=True)
	tues_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='tues_l8',default=None,null=True)

	wed_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l1',default=None,null=True)
	wed_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l2',default=None,null=True)
	wed_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l3',default=None,null=True)
	wed_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l4',default=None,null=True)
	wed_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l5',default=None,null=True)
	wed_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l6',default=None,null=True)
	wed_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l7',default=None,null=True)
	wed_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='wed_l8',default=None,null=True)

	thurs_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l1',default=None,null=True)
	thurs_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l2',default=None,null=True)
	thurs_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l3',default=None,null=True)
	thurs_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l4',default=None,null=True)
	thurs_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l5',default=None,null=True)
	thurs_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l6',default=None,null=True)
	thurs_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l7',default=None,null=True)
	thurs_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='thurs_l8',default=None,null=True)

	fri_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l1',default=None,null=True)
	fri_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l2',default=None,null=True)
	fri_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l3',default=None,null=True)
	fri_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l4',default=None,null=True)
	fri_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l5',default=None,null=True)
	fri_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l6',default=None,null=True)
	fri_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l7',default=None,null=True)
	fri_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='fri_l8',default=None,null=True)

	sat_lec1=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l1',default=None,null=True)
	sat_lec2=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l2',default=None,null=True)
	sat_lec3=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l3',default=None,null=True)
	sat_lec4=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l4',default=None,null=True)
	sat_lec5=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l5',default=None,null=True)
	sat_lec6=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l6',default=None,null=True)
	sat_lec7=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l7',default=None,null=True)
	sat_lec8=models.ForeignKey(branch_subjects,on_delete=models.CASCADE,related_name='sat_l8',default=None,null=True)
