#!/usr/bin/env python
# coding: utf-8
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import sys

 # Count the arguments
arguments = len(sys.argv) - 1
# Output argument-wise
position = 1
while (arguments >= position):
    print ("Input %i: %s" % (position, sys.argv[position]))
    position = position + 1

api_input = sys.argv[1]
summoner_string = sys.argv[2]

api_key = api_input
watcher = LolWatcher(api_key)
my_region = 'na1'
string_ID = summoner_string #HULKSMASH1337, SentientAI, slinky boy
lol_tyler_1 = watcher.summoner.by_name(my_region, string_ID)
print(lol_tyler_1)

my_matches = watcher.match.matchlist_by_account(my_region,
                                                lol_tyler_1['accountId'])


count =0;
for matchData in my_matches['matches']:
    count = count +1


participants =[]
alldata = {}
summoners = pd.DataFrame
counter = 0
for allMatch in range(count-1):
    last_match = my_matches['matches'][allMatch]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])
    find_tyler = match_detail['participants']
    for names in match_detail['participantIdentities']:                     
        rowSum = {}                                                         
        rowSum['Game #'] = allMatch                                         
        rowSum['Participant ID']= names['participantId']                    
        rowSum['Summoner Name'] = names['player']['summonerName']
        if names['player']['summonerName'] == string_ID:
            summoner_ID = rowSum['Participant ID']
            for row in find_tyler:
                stats_row = row['stats']
                if stats_row['participantId'] == summoner_ID:
                    instance_df = pd.DataFrame
                    summoner_stats ={}
                    #summoner_stats['outcome'] = stats_row['win']
                    if stats_row['win'] == True:
                        summoner_stats['outcome'] = 1
                    else:
                        summoner_stats['outcome'] = 0
                    summoner_stats['kills'] = stats_row['kills']
                    summoner_stats['deaths'] = stats_row['deaths']
                    summoner_stats['assists'] = stats_row['assists']
                    summoner_stats['totalDamageDealt'] = stats_row['totalDamageDealt']
                    summoner_stats['damageDealtToObjectives'] = stats_row['damageDealtToObjectives']
                    summoner_stats['totalDamageDealtToChampions'] = stats_row['totalDamageDealtToChampions']
                    summoner_stats['goldEarned'] = stats_row['goldEarned']
                    summoner_stats['totalMinionsKilled'] = stats_row['totalMinionsKilled']
                    alldata[counter] = summoner_stats
                    counter = counter +1         


data_transformed_df = pd.DataFrame.from_dict(alldata).T


#data_transformed_df.head()

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np


X = data_transformed_df[['kills','deaths','assists','totalDamageDealt',
              'damageDealtToObjectives','totalDamageDealtToChampions','goldEarned','totalMinionsKilled']]
y = data_transformed_df['outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y)


from sklearn.metrics import classification_report
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)
y_prob = y_prob[:,1]
print(classification_report(y_test, y_pred))


feature_imp = pd.Series(model.feature_importances_,index=X.columns).sort_values(ascending=False)
import seaborn as sns
import matplotlib.pyplot as plt
plot1 = plt.figure(1)
sns.barplot(x=feature_imp,y=feature_imp.index)
plt.xlabel('Feature Importance')
plt.ylabel('Features')
plt.title(string_ID)


# df2 = data_transformed_df.iloc[[0]]
# DF1 = df2.drop(columns=['outcome'])
mean_data = data_transformed_df.head(5).mean(axis=0)
df_final = mean_data.to_frame().T.drop(columns=['outcome'])
df_final


y_pred = model.predict(df_final)
if y_pred == 1:
    print('The predicted outcome of the next game based on aggregate data over 5 games will be a win')
else:
    print('The predicted outcome of the next game based on aggregate data over 5 games will be a loss')



#watcher.spectator.by_summoner(my_region,lol_tyler_1['id'])
#plt.plot(y_test,'o', color='black')




