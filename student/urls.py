from django.urls import path,re_path
from . import views
app_name='student'

urlpatterns = [
    path('', views.index, name='index'),
    #re_path(r'^$',views.index,name="index"),
	re_path(r'^login/',views.login,name='login'),
    path('logout/',views.logout),
    path('timetable/',views.timetable),
    path('subject/',views.subject),
    path('attendance/',views.attendance),
    path('about/',views.about),
]
