from .models import studentlogin, student_marks

def get_first_student()->studentlogin| None:
    try:
        return studentlogin.stud_obj.first()
    except:
        return None


