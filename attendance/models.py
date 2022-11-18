from django.db import models
from django.utils import timezone
# Create your models here.
class mark_attendance(models.Model):
    student=models.ForeignKey("student.studentlogin",on_delete=models.CASCADE)
    subject=models.ForeignKey("branch.branch_subjects",on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    present=models.BooleanField("Present")

    def __str__(self):
        return str(self.student)+":"+str(self.date)
