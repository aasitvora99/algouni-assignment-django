from django.db import models
from django.contrib.auth.models import User

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
class Problem(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    tags = models.ManyToManyField('Tag')
    time_limit = models.DurationField()
    languages_supported = models.CharField(max_length=100)
    boilerplate_code = models.TextField()
    test_cases = models.ManyToManyField('TestCase')

class Tag(models.Model):
    name = models.CharField(max_length=50)

class TestCase(models.Model):
    input = models.TextField()
    expected_output = models.TextField()
    hidden = models.BooleanField(default=False)

class CodeSubmission(models.Model):
    code = models.TextField()
    language = models.CharField(max_length=50, choices=LANGUAGES_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    execution_time = models.DurationField(null=True, blank=True)  

class CodeOutput(models.Model):
    output = models.TextField()
    verdict = models.CharField(max_length=20) 
    code_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE)

class ProblemAttempt(models.Model):
    VERDICT_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('partial_success', 'Partial Success'),
        ('error', 'Error')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES)
    submissions = models.ManyToManyField(CodeSubmission, related_name='attempt')


class TestCaseResult(models.Model):
    VERDICT_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ]
    attempt = models.ForeignKey(ProblemAttempt, on_delete=models.CASCADE, related_name='results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    output = models.TextField()
    verdict = models.CharField(max_length=20, choices= VERDICT_CHOICES)