from rest_framework import serializers
from .models import Problem, TestCase, CodeSubmission, CodeOutput, Tag 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',) 

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
            tag, _ = Tag.objects.get_or_create(**tag_data)
            problem.tags.add(tag)  

        for test_case_data in test_cases_data:
            test_case = TestCase.objects.create(**test_case_data)
            problem.test_cases.add(test_case) 

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
