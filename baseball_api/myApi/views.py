from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
from .pybaseballgit.pybaseball import top_prospects, standings, batting_stats, playerid_lookup, bwar_bat, bwar_pitch, \
    pitching_stats, rosters


@api_view(['PUT'])
def topProspects(request):
    conv = lambda i: i or None
    team = conv(request.data.get('team'))
    playerType = conv(request.data.get("playerType"))
    prospects = top_prospects(team, playerType)
    prospects = prospects.fillna(0).groupby('Rk').apply(lambda x: x.to_dict(orient='records')[0])
    return Response({'prospects': prospects})


@api_view(['PUT'])
def getStandings(request):
    conv = lambda i: i or None
    date = int(conv(request.data.get('date')))
    currentStandings = standings(date)
    for i, s in enumerate(currentStandings):
        currentStandings[i]['L'] = currentStandings[i]['L'].astype(int)
        currentStandings[i] = s.groupby('Tm').apply(
            lambda x: x.to_dict(orient='records')[0])

    return Response({'standings': currentStandings})


@api_view(['PUT'])
def getBatting(request):
    p = playerid_lookup(request.data.get('lastName'), request.data.get('firstName'))
    firstYear = p['mlb_played_first'][0]
    lastYear = p['mlb_played_last'][0]
    key = str(p['key_fangraphs'][0])
    bWar = bwar_bat().fillna(0)
    bWar = bWar.loc[bWar['player_ID'] == p['key_bbref'][0]].groupby('year_ID').apply(
        lambda x: x.to_dict(orient='records')[0])
    fangraphsStats = batting_stats(firstYear, lastYear, qual=10, players=key).fillna(0).groupby('Season').apply(
        lambda x: x.to_dict(orient='records')[0])

    return Response({'fangraphs': fangraphsStats, 'bwar': bWar})


@api_view(['PUT'])
def getWar(request):
    p = playerid_lookup(request.data.get('lastName'), request.data.get('firstName'), fuzzy=True)
    firstYear = p['mlb_played_first'][0]
    lastYear = p['mlb_played_last'][0]
    key = str(p['key_fangraphs'][0])
    bWarHit = bwar_bat().fillna(0)
    bWarPitch = bwar_pitch().fillna(0)

    try:
        bWarHit = bWarHit.loc[bWarHit['player_ID'] == p['key_bbref'][0]].groupby('year_ID').apply(
            lambda x: x.to_dict(orient='records')[0])
    except:
        bWarPitch = []

    try:
        fangraphsHitting = batting_stats(firstYear, lastYear, qual=10, players=key).fillna(0).groupby('Season').apply(
            lambda x: x.to_dict(orient='records')[0])
    except:
        fangraphsHitting = []

    try:
        bWarPitch = bWarPitch.loc[bWarPitch['player_ID'] == p['key_bbref'][0]].groupby('year_ID').apply(
            lambda x: x.to_dict(orient='records')[0])
    except:
        bWarPitch = []

    try:
        fangraphsPitch = pitching_stats(firstYear, lastYear, qual=10, players=key).fillna(0).groupby('Season').apply(
            lambda x: x.to_dict(orient='records')[0])
    except:
        fangraphsPitch = []

    return Response({'fangraphsHitting': fangraphsHitting, 'brefHitting': bWarHit, 'fangraphsPitching': fangraphsPitch,
                     'brefPitching': bWarPitch})


@api_view(['PUT'])
def getRoster(request):
    conv = lambda i: i or None
    date = int(conv(request.data.get('date')))
    roster = rosters(date)
    return Response({'roster': roster})
