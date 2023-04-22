from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget
from datetime import datetime
import pandas as pd
from erp.models import course
from branch.models import branch_detail
from .models import studentlogin
from import_export.results import RowResult

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
        if row['studentid']==None:
            pass          
        course_name = row.get('course')
        branch_name = row.get('branch')
        section=row.get('section')
        batch=row.get('batch')

        if "DOB" in row:
            dob_string = row["DOB"] 
            dob_object=pd.to_datetime(dob_string).date()
            row["DOB"] = dob_object

        if "DOA" in row:
        
            doa_string = row["DOA"]
            doa_object =pd.to_datetime(doa_string).date()
            row["DOA"] = doa_object

        try:
            row['course'] = course.course_obj.get(name=course_name)
            row['branch'] = branch_detail.branch_obj.get(name=branch_name,section=section,batch=batch).pk
        except :
            kwargs["result"].append_row_error('Invalid details', row, course_name)

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(StudentloginResource, self).import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            # Add a column with the error message
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result
    
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if result.has_errors():
            print('There were errors during the import process. Please check the errors below.')
            for error in result.row_errors():
                print(error)
        else:
            print('Import completed successfully.')
