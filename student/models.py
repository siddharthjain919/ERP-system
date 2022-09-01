from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class studentlogin(models.Model):
    studentid=models.CharField(max_length=20)
    studentpwd=models.CharField(max_length=15, validators=[
            MinLengthValidator(8, 'the field must contain at least 50 characters')
            ])
    isactive=models.IntegerField(null=True)

    def __str__(self):
        return self.studentid

    stud_obj = models.Manager()
