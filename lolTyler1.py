# -*- coding: utf-8 -*-
"""
lolTyler1 toplane challenger api
"""
from riotwatcher import LolWatcher, ApiError
import pandas as pd

# Set global APi
api_key = 'RGAPI-e2cb1bb5-5d04-4818-a616-403aef6b385c'
watcher = LolWatcher(api_key)
my_region = 'na1'

lol_tyler_1 = watcher.summoner.by_name(my_region, 'HULKSMASH1337')
print(lol_tyler_1)

# Return the rank status for Doublelift
#my_ranked_stats = watcher.league.by_summoner(my_region, lol_tyler_1['id'])
#print(my_ranked_stats)

#Access match data
my_matches = watcher.match.matchlist_by_account(my_region, lol_tyler_1['accountId']) #prints out every game
# print(my_matches['matches'])
count =0;
for matchData in my_matches['matches']:
    count = count +1

print(count)
df=[]
dfSum = []
for allMatch in range(5):  #loop over matches: use range(count) to get all match data last 100 games
    last_match = my_matches['matches'][allMatch] #I think I have to iterate here over ever 
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])
    participants =[]
    #print(df)
    #print(dfSum)
    for row in match_detail['participants']:
        part_row ={}
        part_row['Game #'] = allMatch
        part_row['champion'] = row['championId']
        part_row['win'] = row['stats']['win']
        participants.append(part_row)
        df = pd.DataFrame(participants)
        summoners = []
        for names in match_detail['participantIdentities']:
            rowSum = {}
            rowSum['Game #'] = allMatch
            rowSum['Participant ID']= names['participantId']
            rowSum['Summoner Name'] = names['player']['summonerName']
            summoners.append(rowSum)
            dfSum = pd.DataFrame(summoners)
            sumNames = rowSum['Summoner Name']

    print(sumNames.find('HULKSMASH1337'))
