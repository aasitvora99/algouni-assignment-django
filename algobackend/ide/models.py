from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard')
    ]
    LANGUAGES_CHOICES = [
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('python', 'Python')
    ]
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    tags = models.ManyToManyField('Tag')
    time_limit = models.DurationField()
    languages_supported = models.CharField(max_length=100)
    boilerplate_code = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=50)
    

def get_default_problem():
    return Problem.objects.get_or_create(title="Default Problem")[0] 
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default=get_default_problem) 
    input = models.TextField()
    expected_output = models.TextField()
    hidden = models.BooleanField(default=False) 

class CodeSubmission(models.Model):
    code = models.TextField()
    language = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

class CodeOutput(models.Model):
    output = models.TextField()
    verdict = models.CharField(max_length=20) 
    code_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE)
