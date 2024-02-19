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
    tags = TagSerializer(many=True) 
    test_cases = TestCaseSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        test_cases_data = validated_data.pop('test_cases', [])

        problem = Problem.objects.create(**validated_data)

        for tag_data in tags_data:
            Tag.objects.create(problem=problem, **tag_data)

        for test_case_data in test_cases_data:
            TestCase.objects.create(problem=problem, **test_case_data)

        return problem  

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
