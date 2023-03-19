from django.urls import path,include
from . import views

app_name='teacher'

urlpatterns = [
    path('logout/',views.logout,name='logout'),
    path('login/',views.login,name='login'),
    path('timetable/',views.timetable,name="timetable"),
	path('attendance/',include('attendance.urls')),
    path('',views.index,name="index"),
    path("subject/",views.subject,name="subject"),
    path('about/',views.about,name="about"),
    path('your-timetable/',views.teachertimetable,name="teacher_timetable"),
    path('forget/',views.forget,name='forget'),
    path('mail/',views.forgot_mail),
    path('marks/',views.marks,name="marks"),
    path('marks-studentlist',views.studentlist),
    path('mark-marks',views.mark_marks),
    path('add-paper',views.addPaper),
    path('lds',views.lds),
    path('lds-form',views.ldsform),
    path('topics',views.load_topics), ##ajax from ldsform ##
]
