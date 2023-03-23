from django.test import TestCase
from datetime import date
from .models import studentlogin
from branch.models import branch_detail

class StudentLoginTestCase(TestCase):
    
    def setUp(self):
        self.branch=branch_detail.branch_obj.create(
            
        )
        self.student = studentlogin.stud_obj.create(
            studentid='1234',
            name='John Doe',
            gender='MALE',
            DOB=date(2000, 1, 1),
            DOA=date.today(),
            course=None,
            personalEmail='johndoe@example.com',
        )
    
    def test_student_login_creation(self):
        self.assertEqual(self.student.studentid, '1234')
        self.assertEqual(self.student.name, 'John Doe')
        self.assertEqual(self.student.gender, 'MALE')
        self.assertEqual(self.student.DOB, date(2000, 1, 1))
        self.assertEqual(self.student.personalEmail, 'johndoe@example.com')
        print("student details verified")
        
    def test_student_login_str(self):
        self.assertEqual(str(self.student), '1234')
        print("student str verified.")
    
    def test_student_creation(self):
        self.assertIsInstance(self.student,studentlogin)
        print("Student created successfully.")
