from rest_framework import serializers
from .models import Problem, TestCase, CodeSubmission, CodeOutput, Tag 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__' 

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
class ProblemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True) 
    test_cases = TestCaseSerializer(many=True, read_only=True, exclude=('hidden',))  # Only show non-hidden cases

    class Meta:
        model = Problem
        fields = '__all__'


class CodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = '__all__'

class CodeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeOutput
        fields = '__all__'
