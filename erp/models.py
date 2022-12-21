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

def topics(**kwargs):
    if isinstance(kwargs["instance"],subjects):
        subject=kwargs["instance"]
        kwargs["instance"].topics1={"topic_list":subject.to1.split(',')}
        kwargs["instance"].topics2={"topic_list":subject.to2.split(',')}
        kwargs["instance"].topics3={"topic_list":subject.to3.split(',')}
        kwargs["instance"].topics4={"topic_list":subject.to4.split(',')}
        kwargs["instance"].topics5={"topic_list":subject.to5.split(',')}
class subjects(models.Model):
    code=models.CharField(max_length=6,unique=True)
    subject_name=models.CharField(max_length=50,unique=True)
    course=models.ForeignKey("erp.course",on_delete=models.CASCADE)
    CO_1=models.CharField(max_length=50)
    to1=models.CharField(verbose_name="Topics in Unit 1",max_length=500,help_text="Enter topics seperated by ,")
    topics1=models.JSONField(default=None,editable=False,blank=True,null=True)
    
    CO_2=models.CharField(max_length=50)
    to2=models.CharField(verbose_name="Topics in Unit 2",max_length=500,help_text="Enter topics seperated by ,")
    topics2=models.JSONField(default=None,editable=False,blank=True,null=True)
    
    CO_3=models.CharField(max_length=50)
    to3=models.CharField(verbose_name="Topics in Unit 3",max_length=500,help_text="Enter topics seperated by ,")
    topics3=models.JSONField(default=None,editable=False,blank=True,null=True)
    
    CO_4=models.CharField(max_length=50)
    to4=models.CharField(verbose_name="Topics in Unit 4",max_length=500,help_text="Enter topics seperated by ,")
    topics4=models.JSONField(default=None,editable=False,blank=True,null=True)
    
    CO_5=models.CharField(max_length=50)
    to5=models.CharField(verbose_name="Topics in Unit 5",max_length=500,help_text="Enter topics seperated by ,")
    topics5=models.JSONField(default=None,editable=False,blank=True,null=True)

    def __str__(self):
        return self.subject_name
    
    sub_obj=models.Manager()
    pre_save.connect(topics)
