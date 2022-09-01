from django.db import models
from django.core.validators import MinLengthValidator
from branch.models import branch_detail
# Create your models here.
class teacherlogin(models.Model):
    teacherid=models.CharField(max_length=20)
    teacherpwd=models.CharField(max_length=15, validators=[
            MinLengthValidator(8, 'the field must contain at least 8 characters')
            ])
    isactive=models.IntegerField(null=True)
    cc_of_branch=models.ForeignKey(branch_detail,on_delete=models.CASCADE)
    def __str__(self):
        return self.teacherid

    teach_obj = models.Manager()
