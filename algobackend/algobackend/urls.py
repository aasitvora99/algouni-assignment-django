from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ide.views import *

router = routers.DefaultRouter()
# router.register(r'problems', ProblemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/problems/create/', CreateProblemView.as_view()), 
    path('api/', include(router.urls)), 
    path('api/execute/', ExecuteCodeView.as_view()),
    path('api/submissions/', UserSubmissionsView.as_view()),
    path('api/problems/', ProblemListView.as_view()), 
    path('api/problems/<int:pk>/', ProblemDetailView.as_view()), 
]
