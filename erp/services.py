from .models import subjects, course

def get_first_subject()->subjects| None:
    try:
        return subjects.sub_obj.first()
    except:
        return None
    
def get_first_course()->course|None:
    try:
        return course.course_obj.first()
    except:
        return None
    