import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, permissions, status, response
from .models import Problem, CodeSubmission, CodeOutput
from .serializers import ProblemSerializer, CodeSubmissionSerializer, CodeOutputSerializer

class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

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

class CreateProblemView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser] 
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            data = JSONParser().parse(request)
            return Response({"message": "Received JSON Data"}, status=status.HTTP_200_OK)

        elif request.content_type == 'application/x-www-form-urlencoded':
            data = FormParser().parse(request)
            return Response({"message": "Received Form Data"}, status=status.HTTP_200_OK)

        elif request.content_type.startswith('multipart/'): 
            data = MultiPartParser().parse(request)
            return Response({"message": "Received multipart Data"}, status=status.HTTP_200_OK)

        else:
            return response.Response(
                {"error": "Unsupported Content-Type"}, 
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
