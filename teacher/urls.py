from django.urls import path,re_path
from . import views

app_name='teacher'

urlpatterns = [
    path('homepage/', views.index, name='index'),
    path('logout/',views.logout,name='logout'),
    path('login/',views.login,name='login'),
    path('timetable/',views.timetable,name="timetable"),
	path('attendance/',views.attendance,name="attendance"),
    re_path(r'^$',views.index,name="index"),
	path('update/',views.update,name="update"),
    path('subject/add/',views.add,name="add"),
    path("subject/",views.subject,name="subject"),
	path("coordinator/login/",views.coordinatorlogin,name="coordinator"),
    path('about/',views.about,name="about"),
    path('mark_attendance/',views.mark,name="mark"),
    path('your-timetable/',views.teachertimetable,name="teacher_timetable"),
]
