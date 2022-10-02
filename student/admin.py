from django.contrib import admin
from .models import studentlogin
from import_export.admin import ImportExportModelAdmin


class studentloginAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	print(ImportExportModelAdmin)
admin.site.register(studentlogin,studentloginAdmin)
