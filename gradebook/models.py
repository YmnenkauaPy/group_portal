from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'grade', 'created_at')

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.grade}'
    
class ReportCard(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    term = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.student} - {self.term}'
    
    def get_grades(self):
        return self.grade_set.all()