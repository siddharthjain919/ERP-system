from .models import studentlogin, student_marks

def get_first_student()->studentlogin| None:
    try:
        return studentlogin.stud_obj.first()
    except:
        return None
    
def get_student_by_user(username:str)->studentlogin:
    return studentlogin.stud_obj.get(studentid=username)



