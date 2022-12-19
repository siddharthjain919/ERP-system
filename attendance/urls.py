
from django.urls import path
app_name='attendance'
from . import views
urlpatterns=[
    path('',views.attendance_form,name="attendance_form"),
    # path('department/',views.load_department_details,name='ajax-load-department'),
    path('branch/',views.load_branch_details,name='ajax-load-branch'),
    path('subject/',views.load_subject_details,name='ajax-load-subject'),
    path('studentlist',views.studentlist,name='studentlist'),
    path('mark',views.mark)
]