from django.contrib import admin

# Register your models here.
from .models import subjects,branch_detail

admin.site.register(branch_detail)
admin.site.register(subjects)