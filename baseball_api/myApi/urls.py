from django.urls import path, include
from . import views

urlpatterns = [
    path('topProspects/', views.topProspects, name='topProspects'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]