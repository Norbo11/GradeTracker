from django.contrib.auth.models import User
from django.db import models

HEATHCOTE = "HEA"
SUTTON = "SUT"
CLARK = "CLA"
BUTTINGER = "BUT"
DAMES = "DAM"
DARLINGTON = "DAR"
ROBERTSON = "ROB"
JEGEN = "JEG"
TEACHERS_LIST = (

                 (HEATHCOTE, "Mr. Heathcote"),
                 (SUTTON, "Mr. Sutton"),
                 (CLARK, "Mr. Clark"),
                 (BUTTINGER, "Mr. Buttinger"),
                 (DAMES, "Mr. Dames"),
                 (DARLINGTON, "Mrs. Darlington"),
                 (ROBERTSON, "Ms. Robertson"),
                 (JEGEN, "Ms. Jegen")
                 )

GRADES_LIST = list()
for grade in reversed(range(1, 8)):
    if (grade == 1): GRADES_LIST.append((1, "U"))
    else: GRADES_LIST.append((grade, chr(72 - grade))) ##72 = 'H' in ASCII, taking away the value of grade will give the grade char we need

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.get_username()


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Unit(models.Model):
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    unit = models.ForeignKey(Unit)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentGrade(models.Model):
    student = models.ForeignKey(Student)
    chapter = models.ForeignKey(Chapter)
    predicted_grade = models.IntegerField(choices=GRADES_LIST)
    test_grade = models.IntegerField(choices=GRADES_LIST)

    def __str__(self):
        return self.student.user.username + " - " + self.chapter.name + " - " + "[" + str(self.predicted_grade) + ", " + str(self.test_grade) + "]"

class StudiedSubject(models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    teacher1 = models.CharField(max_length=100, choices=TEACHERS_LIST)
    teacher2 = models.CharField(max_length=100, choices=TEACHERS_LIST)

    def __str__(self):
        return self.subject.name


