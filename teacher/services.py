from .models import teacherlogin

def get_first_teacher()->teacherlogin| None:
    try:
        return teacherlogin.teach_obj.first()
    except:
        return None
    
def get_teacher_by_user(username:str)->teacherlogin:
    return teacherlogin.teach_obj.get(teacherid=username)