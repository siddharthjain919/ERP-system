from django.contrib import admin

# Register your models here.
from . models import teacherlogin,teacher_timetable

admin.site.register(teacherlogin)
admin.site.register(teacher_timetable)
