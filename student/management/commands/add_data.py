from django.core.management.base import BaseCommand
import pandas as pd
from student.models import studentlogin
from sqlalchemy import create_engine
class Command(BaseCommand):
	help="For adding data to excel file"
	def handle(self,*args,**options):
		excel_file='book1.xlsx'
		df=pd.read_excel(excel_file)
		#print(df)
		engine=create_engine('sqlite:///db.sqlite3')
		df.to_sql(studentlogin._meta.db_table,if_exists='append',con=engine,index=False)
