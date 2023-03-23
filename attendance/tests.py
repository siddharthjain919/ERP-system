from datetime import datetime
from django.test import TestCase
from .models import mark_attendance
from student.services import get_first_student
from erp.tests import SubjectTestCase
from teacher.services import get_first_teacher
# Create your tests here.


class TestCaseAttendance(TestCase):
    def test_mark_attendance(self):
        student=get_first_student()
        subject=SubjectTestCase().setUp()
        teacher=get_first_teacher()
        test_attendance=mark_attendance.attend_obj.create(
                student=student,
                session=2022,
                subject=subject,
                date=datetime.now(),
                present=True,
                lecture_number=6,
                semester=5,
                teacher=teacher,
            )
        self.assertIsInstance(test_attendance,mark_attendance)
