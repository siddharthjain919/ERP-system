from django.db import models
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import Group
def create_group(**kwargs):
    if kwargs["created"]  and (isinstance(kwargs["instance"],course)):
        # name=kwargs["instance"]
        Group.objects.create(name=kwargs["instance"].name)
class course(models.Model):
    name=models.CharField(max_length=20,primary_key=True)
    Course_Objective_1=models.CharField(max_length=50)
    Course_Objective_2=models.CharField(max_length=50)
    Course_Objective_3=models.CharField(max_length=50)
    Course_Objective_4=models.CharField(max_length=50)
    Course_Objective_5=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    post_save.connect(create_group)
    course_obj=models.Manager()

class subjects(models.Model):
    code=models.CharField(max_length=6,unique=True)
    subject_name=models.CharField(max_length=50,unique=True)
    course=models.ForeignKey("erp.course",on_delete=models.CASCADE)
    CO_1=models.CharField(max_length=50)
    
    CO_2=models.CharField(max_length=50)
    
    CO_3=models.CharField(max_length=50)
    
    CO_4=models.CharField(max_length=50)
    
    CO_5=models.CharField(max_length=50)
    
    def __str__(self):
        return self.subject_name
    
    sub_obj=models.Manager()
    
