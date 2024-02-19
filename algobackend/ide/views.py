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
        data = self.parse_data(request)

        serializer = ProblemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def parse_data(self, request):
        if request.content_type == 'application/json':
            return JSONParser().parse(request)
        elif request.content_type == 'application/x-www-form-urlencoded':
            return FormParser().parse(request)
        elif request.content_type.startswith('multipart/'): 
            return MultiPartParser().parse(request)
        else:
            raise TypeError("Unsupported Content-Type") 
