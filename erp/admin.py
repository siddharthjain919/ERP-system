from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(course)
admin.site.register(subjects)
admin.site.register(question_paper)
admin.site.register(achievements)



