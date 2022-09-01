from django.db import models
class lec(models.Model):
    sub=models.CharField(max_length=25)
    fac=models.CharField(max_length=25)
    loc=models.CharField(max_length=25)
    
class branch(models.Model):
    name=models.CharField(max_length=25)
    batch=models.IntegerField()
    #day=[lec() for i in range(8)]
    timetable=[[lec() for i in range(8)] for i in range(6)]

