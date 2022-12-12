from django.forms import ModelForm
from django import forms
from .models import branch_subjects,branch_detail
class branch_subject_form(ModelForm):
    class Meta:
        model=branch_subjects
        fields='__all__'
        
        labels={
            "branch":"Branch",
            "branch_subject":"Subject",
            "subject_teacher":"Faculty",
            "NOLR1":"No of Lecture For Objective 1",
            "NOLR2":"No of Lecture For Objective 2",
            "NOLR3":"No of Lecture For Objective 3",
            "NOLR4":"No of Lecture For Objective 4",
            "NOLR5":"No of Lecture For Objective 5",
        }
class branch_timetable_form(ModelForm):
    class Meta:
        model=branch_detail
        fields='__all__'