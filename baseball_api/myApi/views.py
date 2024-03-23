import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .pybaseballgit.pybaseball import top_prospects

@api_view(['PUT'])
def topProspects(request):
    conv = lambda i: i or None
    team = conv(request.data.get('team'))
    playerType = conv(request.data.get("playerType"))
    prospects = top_prospects(team, playerType)
    prospects = prospects.fillna(0).groupby('Rk').apply(lambda x: x.to_dict(orient='records')[0])
    return Response({'prospects': prospects})
