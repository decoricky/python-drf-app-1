from django.urls import path

from . import views

app_name = 'apiv1'
urlpatterns = [
    path('bmonster/', views.UpdateDataAPIView.as_view()),
    path('bmonster/studio/', views.StudioListAPIView.as_view()),
    path('bmonster/performer/', views.PerformerListAPIView.as_view()),
    path('bmonster/program/', views.ProgramListAPIView.as_view()),
    path('bmonster/schedule/', views.ScheduleListAPIView.as_view()),
]
