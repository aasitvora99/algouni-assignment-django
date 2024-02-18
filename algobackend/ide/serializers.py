from rest_framework import serializers
from .models import Problem, TestCase, CodeSubmission, CodeOutput

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class CodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = '__all__'

class CodeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeOutput
        fields = '__all__'
