from django.urls import path
from . import views

urlpatterns = [
    path('api/test-submission/', views.test_submission, name='test_submission'),
]