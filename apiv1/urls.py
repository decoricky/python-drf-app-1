from django.urls import path

from . import views

app_name = 'apiv1'
urlpatterns = [
    path('studio/', views.StudioListAPIView.as_view())
]
