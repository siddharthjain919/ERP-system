from django.urls import path
from . import views

app_name='student'

urlpatterns = [
    path('', views.index, name='index'),
	path('login/',views.login,name='login'),
    path('logout/',views.logout),
    path('timetable/',views.timetable),
    path('subject/',views.subject),
    path('attendance/',views.attendance),
    path('about/',views.about),
    path('forget/',views.forget,name='forget'),
    path('mail/',views.forgot_mail),
]
