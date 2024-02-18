import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CodeSubmission, CodeOutput # Assuming you have the serializers defined
from .serializers import CodeSubmissionSerializer, CodeOutputSerializer

class ExecuteCodeView(APIView):
    def post(self, request):
        code = request.data.get('code')
        language = request.data.get('language')
        test_case_input = request.data.get('input')

        # ... Logic to execute code based on 'language' ...
        #     (This is where things get language-specific) 

        # Assuming Python execution for simplicity:
        try:
            output = subprocess.check_output(['python', '-c', code], input=test_case_input, encoding='utf-8')
            verdict = 'Pass'  # Adjust if the output needs verification
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            verdict = 'Runtime Error' 

        # Store CodeSubmission and CodeOutput in the database ... 

        return Response({
            'output': output,
            'verdict': verdict
        })

class UserSubmissionsView(APIView):
    def get(self, request):
        user = request.user  # Assuming authentication 
        submissions = CodeSubmission.objects.filter(user=user)
        submissions_data = CodeSubmissionSerializer(submissions, many=True).data

        # Assuming a nested relationship for output in your serializer
        return Response(submissions_data) 
