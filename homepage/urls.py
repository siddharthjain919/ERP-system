from django.urls import path,re_path
from . import views

app_name='homepage'

urlpatterns = [
    path('homepage', views.index, name='index'),
    re_path(r'^$',views.index,name="index"),
]
