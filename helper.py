from riotwatcher import LolWatcher, ApiError
import pandas as pd
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def which_region():
    print('Which region do you want, na1 or euw1?')
    region_input = input('Enter region:')
    return region_input

def import_data():
    arguments = len(sys.argv) - 1
    position = 1
    while (arguments >= position):
        print ("Input %i: %s" % (position, sys.argv[position]))
        position = position + 1
        api_input = sys.argv[1]
        summoner_string = sys.argv[2]
    return api_input,summoner_string


class RiotAccount:
    def __init__(self,input_api,get_summoner,my_region):
        self.api = input_api
        self.summoner = get_summoner
        self.region = my_region
        self.watcher = LolWatcher(self.api)
        self.summoner_info = {}
        self.match_count = 0
        self.my_matches = {}
        self.save_model = {}

    def summoner_data(self):
        summoner_data_info = self.watcher.summoner.by_name(self.region, self.summoner)
        print(summoner_data_info)
        self.summoner_info = summoner_data_info

    def get_match_count(self):
        match_list = self.watcher.match.matchlist_by_account(self.region,
                                           self.summoner_info['accountId'])
        self.my_matches = match_list
        count =0;
        for matchData in self.my_matches['matches']:
            count = count +1
        self.match_count = count

    def get_match_data(self):
        all_data = {}
        counter = 0
        for allMatch in range(self.match_count-1):
            last_match = self.my_matches['matches'][allMatch]
            match_detail = self.watcher.match.by_id(self.region,last_match['gameId'])
            find_summoner = match_detail['participants']
            for names in match_detail['participantIdentities']:
                rowSum = {}
                rowSum['Game #'] = allMatch
                rowSum['Participant ID'] = names['participantId']
                rowSum['Summoner Names'] = names['player']['summonerName']
                if names['player']['summonerName'] == self.summoner:
                    summoner_ID = rowSum['Participant ID']
                    for row in find_summoner:
                        stats_row = row['stats']
                        if stats_row['participantId'] == summoner_ID:
                            summoner_stats = {}
                            if stats_row['win'] == True:
                                summoner_stats['outcome'] = 1
                            else:
                                summoner_stats['outcome'] = 0
                            summoner_stats['kills'] = stats_row['kills']
                            summoner_stats['deaths']  = stats_row['deaths']
                            summoner_stats['assists'] = stats_row['assists']
                            summoner_stats['total Damage Dealt'] = stats_row['totalDamageDealt']
                            summoner_stats['Objective Damage'] = stats_row['damageDealtToObjectives']
                            summoner_stats['Damage to Champs'] = stats_row['totalDamageDealtToChampions']
                            summoner_stats['Gold Earned'] = stats_row['goldEarned']
                            summoner_stats['total Minions'] = stats_row['totalMinionsKilled']
                            summoner_stats['Damage Taken'] = stats_row['totalDamageTaken']
                            all_data[counter] = summoner_stats
                            counter += 1
                            #print(counter)
        data_transformed_df = pd.DataFrame.from_dict(all_data).T
        return data_transformed_df

    def Decision_Tree_Class(self,data_transformed_df):
        x = data_transformed_df[['kills','deaths','assists','total Damage Dealt',
                                 'Objective Damage','Damage to Champs',
                                'Gold Earned','total Minions','Damage Taken']]
        y = data_transformed_df['outcome']
        x_train,X_test,y_train,y_test = train_test_split(x,y)
        model = DecisionTreeClassifier()
        model.fit(x_train,y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_log_proba(X_test)
        y_prob = y_prob[:,1]
        print(classification_report(y_test,y_pred))
        self.save_model = model
        return x

    def calculate_win_loss(self,data_transformed_df):
        mean_data = data_transformed_df.head(10).mean(axis=0)
        df_final = mean_data.to_frame().T.drop(columns=['outcome'])
        y_pred = self.save_model.predict(df_final)
        if y_pred == 1:
            print('Win: based off last 10 games')
        else:
            print('Loss: based off last 10 games')

    def plot_data(self,X):
        feature_imp = pd.Series(self.save_model.feature_importances_,index=X.columns).sort_values(ascending=False)
        plot1 = plt.figure(1)
        sns.barplot(x=feature_imp,y=feature_imp.index)
        plt.xlabel('Feature Importance')
        plt.ylabel('Features')
        plt.title(self.summoner)
        plt.draw()
        plt.show()
