from .models import teacherlogin

def get_first_teacher()->teacherlogin| None:
    try:
        return teacherlogin.teach_obj.first()
    except:
        return None