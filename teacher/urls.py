from django.urls import path,re_path
from . import views

app_name='teacher'

urlpatterns = [
    path('homepage/', views.index, name='index'),
    path('logout/',views.logout,name='logout'),
    path('login/',views.login,name='login'),
    path('timetable/',views.timetable,name="timetable"),
    re_path(r'^$',views.index,name="index"),
	path('update/',views.update,name="update"),
    path('subject/add/',views.add,name="add"),
    path("subject/",views.subject,name="subject"),
]
