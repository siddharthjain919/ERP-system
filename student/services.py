from .models import studentlogin, student_marks,practical
from typing import Union
from django.db.models import QuerySet

def get_first_student()->Union[studentlogin,None]:
    try:
        return studentlogin.stud_obj.first()
    except:
        return None
    
def get_student_by_user(username:str)->studentlogin:
    return studentlogin.stud_obj.get(studentid=username)

def get_practicals(subject)->QuerySet[practical]:
    return practical.objects.filter(subject=subject).order_by('is_evaluated')
