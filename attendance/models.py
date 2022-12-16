from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class mark_attendance(models.Model):
    student=models.ForeignKey("student.studentlogin",on_delete=models.CASCADE)
    subject=models.ForeignKey("erp.subjects",on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    present=models.BooleanField("Present")
    lecture_number=models.IntegerField(validators=[MaxValueValidator(8),MinValueValidator(1)])
    
    def __str__(self):
        return str(self.student)+":"+str(self.date)
    class Meta:
        unique_together=[["student","date","lecture_number"]]
    
    attend_obj=models.Manager()
