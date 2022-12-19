from django.contrib import admin
from .models import studentlogin
from import_export.admin import ImportExportModelAdmin,ImportExportMixin
import pandas as pd
from sqlalchemy import create_engine
'''class Command(BaseCommand):
	help="For adding data to excel file"
	def handle(self,*args,**options):
		excel_file='book1.xlsx'
		df=pd.read_excel(excel_file)
		#print(df)
		engine=create_engine('sqlite:///db.sqlite3')
		df.to_sql(studentlogin._meta.db_table,if_exists='append',con=engine,index=False)
'''
# class studentloginAdmin(ImportExportModelAdmin,admin.ModelAdmin):
# 	#print(dir(ImportExportModelAdmin))
# 	engine=create_engine('sqlite:///db.sqlite3')
# 	exclude=("id",)
# 	list_display=["studentid","student_name","studentpwd","branch","email"]

admin.site.register(studentlogin)
