from django.contrib import admin

# Register your models here.
from .models import *

class branch_detailAdmin(admin.ModelAdmin):
    change_form_template = "change_form.html"
    def response_change(self, request, obj):
        if "endsem" in request.POST:
            print("inside if",obj,type(obj))
            if obj.semester==8:
                pass
            else:
                obj.semester+=1
                obj.save()
                try:
                    branch_subjects.branch_sub_obj.filter(branch=obj).delete()
                except:
                    pass
        return super().response_change(request, obj)

admin.site.register(branch_detail,branch_detailAdmin)
admin.site.register(branch_subjects)
