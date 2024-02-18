from django.contrib import admin
from .models import Problem, TestCase, CodeSubmission, CodeOutput

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(CodeSubmission)
admin.site.register(CodeOutput)
