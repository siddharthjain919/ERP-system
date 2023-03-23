from django.test import TestCase
from django.contrib.auth.models import User,Group
from .models import teacherlogin

class TeacherLoginTestCase(TestCase):
    def setUp(self):
        self.teacher = teacherlogin.teach_obj.create(
            teacherid='T1',
            name='John Doe',
            pwd='testpassword',
            blood_group='O+',
            gender='MALE',
            email='john.doe@example.com'
        )
        return self.teacher

    def teacher_created(self):
        self.assertIsInstance(self.teacher,teacherlogin)

    def test_create_user_on_teacher_save(self):
        self.assertIs(User.objects.filter(username='T1').exists(), True)
        self.teacher.save()
        print('Teacher User created')
    
    def test_teacher_in_group(self):
        self.assertIs(User.objects.filter(username=self.teacher.teacherid)[0].groups.filter(name='teacher').exists(),True)
        print('User found in group teacher')

    def test_delete_user_on_teacher_delete(self):
        self.teacher.delete()
        self.assertIs(User.objects.filter(username='T1').exists(), False)
        print("User deleted on teacher deletion")
    

    def test_password_min_length_validator(self):
        teacher = teacherlogin(
            teacherid='T2',
            name='Jane Doe',
            pwd='short',
            blood_group='O+',
            gender='FEMALE',
            email='jane.doe@example.com'
        )
        with self.assertRaises(ValueError):
            print('Short password passed.')




    
