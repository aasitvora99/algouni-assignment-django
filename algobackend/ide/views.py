import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CodeSubmission, CodeOutput
from .serializers import CodeSubmissionSerializer, CodeOutputSerializer

class ExecuteCodeView(APIView):
    def post(self, request):
        code = request.data.get('code')
        language = request.data.get('language')
        test_case_input = request.data.get('input')
        try:
            output = subprocess.check_output(['python', '-c', code], input=test_case_input, encoding='utf-8')
            verdict = 'Pass' 
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            verdict = 'Runtime Error' 

        return Response({
            'output': output,
            'verdict': verdict
        })

class UserSubmissionsView(APIView):
    def get(self, request):
        user = request.user  # auth 
        submissions = CodeSubmission.objects.filter(user=user)
        submissions_data = CodeSubmissionSerializer(submissions, many=True).data
        return Response(submissions_data) 
