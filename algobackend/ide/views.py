import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, permissions, status, response
from .models import Problem, TestCase, CodeSubmission, ProblemAttempt, CodeOutput, TestCaseResult
from .serializers import ProblemSerializer, CodeSubmissionSerializer
from django.shortcuts import get_object_or_404


class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if ProblemAttempt.objects.filter(user=self.request.user, problem=self.get_object(), end_time=None).exists():
            context['exclude_test_cases'] = True 
        return context

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

# @shared_task
# def evaluate_code_submission(submission_id):
#     submission = CodeSubmission.objects.get(id=submission_id)
#     problem = submission.problem
#     test_cases = problem.test_cases.all()

#     # ... Code execution (language-specific, use sandboxing!) ...

#     # Update attempt (set end_time and overall verdict - you'll need a function to compute overall_verdict)
#     submission.attempt.end_time = timezone.now()
#     submission.attempt.overall_verdict = calculate_overall_verdict(...)  
#     submission.attempt.save()

# class CodeSubmissionCreateView(APIView):  
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, problem_id):
#         code = request.data.get('code')
#         language = request.data.get('language')
#         problem = get_object_or_404(Problem, pk=problem_id)

#         # Validation ... 

#         problem_attempt, created = ProblemAttempt.objects.get_or_create(  
#             user=request.user,
#             problem_id=problem_id,
#             defaults={'code': code}  # Store submitted code in attempt initially
#         )  

#         submission = CodeSubmission.objects.create(
#             attempt=problem_attempt,
#             user=request.user,
#             problem=problem,
#             code=code,
#             language=language
#         )

#         # Trigger Celery task
#         evaluate_code_submission.delay(submission.id)  

#         return Response({"message": "Code submission received"}, status=status.HTTP_202_ACCEPTED)
