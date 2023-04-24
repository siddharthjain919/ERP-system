from django.urls import path,include
from . import views

app_name='teacher'

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forget/',views.forget,name='forget'),
    path("subject/",views.subject,name="subject"),
    path('timetable/',views.timetable,name="timetable"),
    path('your-timetable/',views.teachertimetable,name="teacher_timetable"),
	path('attendance/',include('attendance.urls')),
    path('about/',views.about,name="about"),
    path('marks/',views.marks,name="marks"),
    path('marks-studentlist',views.studentlist),
    path('mark-marks',views.mark_marks),
    path('add-paper',views.addPaper),
    path('lds',views.lds),
    path('lds-form',views.ldsform),
    path('topics',views.load_topics), ##ajax from ldsform ##
    path('ajax/load-CO',views.load_objectives), ##ajax
    path('lab',views.lab),
]
