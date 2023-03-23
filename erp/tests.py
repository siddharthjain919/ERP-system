from django.test import TestCase
from .models import course, subjects, question_paper


class CourseTestCase(TestCase):
    def setUp(self):
        self.course = course.course_obj.create(
            name="Test Course",
            Course_Objective_1="Objective 1", 
            Course_Objective_2="Objective 2", 
            Course_Objective_3="Objective 3", 
            Course_Objective_4="Objective 4", 
            Course_Objective_5="Objective 5"
        )
        return self.course
    
    def test_course_in_db(self):
        self.assertIsInstance(self.course,course)
        print("course created successfully")


class SubjectTestCase(TestCase):
    def setUp(self):
        course = CourseTestCase().setUp()
        self.subject1 = subjects.sub_obj.create(
            code="SUB001",
            subject_name="Subject 1",
            course=course,
            CO_1="CO1", 
            to1="Topic 1", 
            CO_2="CO2", 
            to2="Topic 2", 
            CO_3="CO3", 
            to3="Topic 3", 
            CO_4="CO4", 
            to4="Topic 4", 
            CO_5="CO5", 
            to5="Topic 5"
        )
        return self.subject1

    def test_subject_creation(self):
        self.assertEqual(self.subject1.__str__(), self.subject1.subject_name)
