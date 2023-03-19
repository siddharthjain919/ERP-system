from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget
from datetime import datetime
import pandas as pd
from erp.models import course
from branch.models import branch_detail
from .models import studentlogin

class CustomForeignKeyWidget(ForeignKeyWidget):
    def get_queryset(self, value, row=None, *args, **kwargs):
        if self.model == branch_detail:
            return self.model.branch_obj.all()
        else:
            return self.model.course_obj.all()
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            try:
                return self.get_queryset(value, row).get(**{self.field: value})
            except Exception as e:
                print(e)


class StudentloginResource(resources.ModelResource):
    course = fields.Field(column_name='course', attribute='course', widget=CustomForeignKeyWidget(course))
    branch = fields.Field(column_name='branch', attribute='branch', widget=CustomForeignKeyWidget(branch_detail))
    class Meta:
        model = studentlogin
        fields = ('studentid', 'name', 'gender', 'DOB', 'DOA', 'course', 'branch','personalEmail','section')
        import_id_fields = ('studentid',)
        skip_unchanged = True
        report_skipped = False
        queryset=studentlogin.stud_obj.all()
    def get_queryset(self):
        return self.Meta.model.stud_obj.all()

    def before_import_row(self, row, **kwargs):
        
        course_name = row.get('course')
        branch_name = row.get('branch')
        section=row.get('section')
        # print(branch_name)
        
        dob_string = row["DOB"]
        dob_object=pd.to_datetime(dob_string, unit='D', origin='1899-12-30').date()
        row["DOB"] = dob_object

        doa_string = row["DOA"]
        doa_object =pd.to_datetime(doa_string, unit='D', origin='1899-12-30').date()
        row["DOA"] = doa_object

        try:
            row['course'] = course.course_obj.get(name=course_name)
            row['branch'] = branch_detail.branch_obj.get(name=branch_name,section=section).pk
        except :
            kwargs["result"].append_row_error('Invalid details', row, course_name)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if result.has_errors():
            print('There were errors during the import process. Please check the errors below.')
            for error in result.row_errors():
                print(error)
        else:
            print('Import completed successfully.')
