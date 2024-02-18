from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ide.views import ExecuteCodeView
from ide.views import UserSubmissionsView

router = routers.DefaultRouter()
# router.register(r'problems', ProblemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('api/execute/', ExecuteCodeView.as_view()),
    path('api/submissions/', UserSubmissionsView.as_view())
]
