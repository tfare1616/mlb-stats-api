from django.urls import path, include
from . import views

urlpatterns = [
    path('topProspects/', views.topProspects, name='topProspects'),
    path('standings/', views.getStandings, name='standings'),
    path('getBatting/', views.getBatting, name='batting'),
    path('getWar/', views.getWar, name='war'),
    path('getRoster/', views.getRoster, name='roster'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]