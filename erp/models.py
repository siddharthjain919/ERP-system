from django.db import models
class subjects(models.Model):
    subject_name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.subject_name
    sub_obj=models.Manager()
