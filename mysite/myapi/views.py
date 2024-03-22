from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pybaseball import pybaseball
import json
import pandas as pd


@api_view(['GET'])
def teams(request):
    topProspects = pybaseball.top_prospects('yankees', None)
    return Response({'message': 'topProspects'})
