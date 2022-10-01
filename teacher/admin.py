from django.contrib import admin

# Register your models here.
from . models import teacherlogin

admin.site.register(teacherlogin)
class teacherloginAdmin(admin.ModelAdmin):
	exclude=("teacherpwd",)
