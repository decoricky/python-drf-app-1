from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from . import views

router = routers.DefaultRouter()
router.register('attendanceHistory', views.AttendanceHistoryViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('auth/jwt/', jwt_views.TokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('bmonster/', views.UpdateDataAPIView.as_view()),
    path('bmonster/', include(router.urls)),
    path('bmonster/studio/', views.StudioListAPIView.as_view()),
    path('bmonster/performer/', views.PerformerListAPIView.as_view()),
    path('bmonster/program/', views.ProgramListAPIView.as_view()),
    path('bmonster/schedule/', views.ScheduleListAPIView.as_view()),
]
