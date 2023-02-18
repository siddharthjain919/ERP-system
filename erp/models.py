from django.db import models
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import Group,User
def create_group(**kwargs):
    if kwargs["created"]  and (isinstance(kwargs["instance"],course)):
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
    code=models.CharField(max_length=12,unique=True)
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

class question_paper(models.Model):
    subject=models.ForeignKey(subjects,on_delete=models.CASCADE)
    session=models.IntegerField()
    semester=models.IntegerField()

    Ques1_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partB=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partC=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partD=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partE=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partF=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partG=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partH=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partI=models.CharField(null=True,blank=True,max_length=120)
    Ques1_partJ=models.CharField(null=True,blank=True,max_length=120)

    Ques1_partA_marks=models.IntegerField(null=True,blank=True)
    Ques1_partB_marks=models.IntegerField(null=True,blank=True)
    Ques1_partC_marks=models.IntegerField(null=True,blank=True)
    Ques1_partD_marks=models.IntegerField(null=True,blank=True)
    Ques1_partE_marks=models.IntegerField(null=True,blank=True)
    Ques1_partF_marks=models.IntegerField(null=True,blank=True)
    Ques1_partG_marks=models.IntegerField(null=True,blank=True)
    Ques1_partH_marks=models.IntegerField(null=True,blank=True)
    Ques1_partI_marks=models.IntegerField(null=True,blank=True)
    Ques1_partJ_marks=models.IntegerField(null=True,blank=True)
    MarksQues1=models.IntegerField()


    Ques2_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques2_partB=models.CharField(null=True,blank=True,max_length=120)
    Ques2_partC=models.CharField(null=True,blank=True,max_length=120)
    Ques2_partD=models.CharField(null=True,blank=True,max_length=120)
    Ques2_partE=models.CharField(null=True,blank=True,max_length=120)

    Ques2_partA_marks=models.IntegerField(null=True,blank=True)
    Ques2_partB_marks=models.IntegerField(null=True,blank=True)
    Ques2_partC_marks=models.IntegerField(null=True,blank=True)
    Ques2_partD_marks=models.IntegerField(null=True,blank=True)
    Ques2_partE_marks=models.IntegerField(null=True,blank=True)
    MarksQues2=models.IntegerField()

    Ques3_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques3_partB=models.CharField(null=True,blank=True,max_length=120)

    Ques3_partA_marks=models.IntegerField(null=True,blank=True)
    Ques3_partB_marks=models.IntegerField(null=True,blank=True)
    MarksQues3=models.IntegerField()

    Ques4_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques4_partB=models.CharField(null=True,blank=True,max_length=120)

    Ques4_partA_marks=models.IntegerField(null=True,blank=True)
    Ques4_partB_marks=models.IntegerField(null=True,blank=True)
    MarksQues4=models.IntegerField()

    Ques5_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques5_partB=models.CharField(null=True,blank=True,max_length=120)

    Ques5_partA_marks=models.IntegerField(null=True,blank=True)
    Ques5_partB_marks=models.IntegerField(null=True,blank=True)
    MarksQues5=models.IntegerField()

    Ques6_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques6_partB=models.CharField(null=True,blank=True,max_length=120)

    Ques6_partA_marks=models.IntegerField(null=True,blank=True)
    Ques6_partB_marks=models.IntegerField(null=True,blank=True)
    MarksQues6=models.IntegerField()

    Ques7_partA=models.CharField(null=True,blank=True,max_length=120)
    Ques7_partB=models.CharField(null=True,blank=True,max_length=120)

    Ques7_partA_marks=models.IntegerField(null=True,blank=True)
    Ques7_partB_marks=models.IntegerField(null=True,blank=True)
    MarksQues7=models.IntegerField()

    total_marks=models.IntegerField(null=True,blank=True)

    question_paper_obj=models.Manager()
    def __str__(self):
        return str(self.subject)+str(self.session)

class achievements(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    issuingOrganization=models.CharField(max_length=150,verbose_name="Issuing Organization")
    issuingYear=models.CharField(max_length=4,verbose_name="Issuing Year")
    link=models.CharField(max_length=250,verbose_name="Achievement Link")
    description=models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.user)+self.description 
    achieve_obj=models.Manager()