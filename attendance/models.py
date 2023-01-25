from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import date
# Create your models here.
class mark_attendance(models.Model):
    student=models.ForeignKey("student.studentlogin",on_delete=models.CASCADE)
    session=models.IntegerField(validators=[MaxValueValidator(int(date.today().year))],default=int(date.today().year),editable=False)
    subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    present=models.BooleanField("Present")
    lecture_number=models.IntegerField(validators=[MaxValueValidator(8),MinValueValidator(1)])
    semester=models.IntegerField(default=1,validators=[MaxValueValidator(8),MinValueValidator(1)],editable=False)
    teacher=models.ForeignKey("teacher.teacherlogin",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.student)+":"+str(self.date)+":"+str(self.lecture_number)
    class Meta:
        unique_together=[["student","date","lecture_number"]]
    
    attend_obj=models.Manager()
