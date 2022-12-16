from django import forms
from taggit.forms import TagWidget
# from bootstrap_datepickerplus import DatePickerInput
from .models import mark_attendance
from erp.models import course,department,subjects
from branch.models import branch_detail
from student.models import studentlogin

from django.urls import reverse_lazy

class mark_attendance_form(forms.ModelForm):
    course=forms.ModelChoiceField(queryset=course.course_obj.all())
    department=forms.ModelChoiceField(queryset=department.department_obj.all())
    branch=forms.ModelChoiceField(queryset=branch_detail.branch_obj.all())
    class Meta:
        model=mark_attendance
        fields=('course','department','branch','subject')

        widgets={
            'course':forms.Select(attrs={'id':'course','class':'form-control'}),
            'department':forms.Select(attrs={'id':'department','class':'form-control','department-queries-url':reverse_lazy('ajax-load')}),
            'branch':forms.Select(attrs={'id':'branch','class':'form-control','branch-queries-url':reverse_lazy('ajax-load-branch')}),
            # 'subject':forms.Select(attrs={'id':'subject','class':'form-control','subject-queries-url':reverse_lazy('ajax-load-subject')}),
            # 'student':forms.Select(attrs={"id":"student",'class':'form-control','subject-queries-url':reverse_lazy('ajax-load-subject')}),
        }
    def __init__(self,*args,**kwargs):

        super().__init__(*args, **kwargs)
        self.fields['department'].queryset=department.department_obj.none()
        self.fields['branch'].queryset=branch_detail.branch_obj.none()
        self.fields['subject'].queryset=subjects.sub_obj.none()
        # self.fields['student'].queryset=studentlogin.stud_obj.none()
        

        