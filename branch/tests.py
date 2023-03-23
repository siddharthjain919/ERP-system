from django.test import TestCase
from .models import branch_detail,branch_subjects
from erp.tests import CourseTestCase, SubjectTestCase

from teacher.tests import TeacherLoginTestCase
# Create your tests here.

class BranchDetailTestCase(TestCase):
    def setUp(self) -> None:
        course=CourseTestCase().setUp()
        self.branch=branch_detail.branch_obj.create(
            name="test_branch",
            batch=2022,
            section='A',
            course=course,
            semester=5,
            PSO_1='test',
            PSO_2='test',
            PSO_3='test',
            PSO_4='test',
            PSO_5='test',
        )
        return self.branch
    
    def branch_in_db(self):
        self.assertIsInstance(self.branch,branch_detail)
        print("branch created successfully")

def BranchSubjectTestCase(TestCase):

    def setup(self):
        self.branch=BranchDetailTestCase().setUp()
        self.subject=SubjectTestCase().setUp()
        self.teacher=TeacherLoginTestCase().setUp()
        self.subject=branch_subjects.branch_sub_obj.create()
    
    