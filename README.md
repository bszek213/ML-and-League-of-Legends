# ML-and-League-of-Legends                                                      
Using ML to predict outcomes of any summoner in league of legends, as well as getting the features that affect their
I used a Decision Tree Classifier 

## Usage
There are two ways of executed the code:terminal or Notebook.

Execute the tyler1_predictor_win_loss.py script in your terminal:
```bash
$ python python tyler1_predictor_win_loss.py "Your-Riot-API" "Summoner_Name_that_you_want_to_eval"
```
OR with the tyler1_predictor_win_loss.ipynb file.

if you use the tyler1_predictor_win_loss.py script the output 
will look something like this:

Input 1: Your-Riot-API
Input 2: Summoner_Name_that_you_want_to_eval


{'id': 'wzoROkOGV256lDuraz1SmF44aWZA23P_2xxNQqGxg0mZLqpn', 'accountId': 'LmXEidbyDIZ39ZzRRAngA7gA6wcxVN1fQEX1PwvyLq2ELFi3vP2ka_4N', 'puuid': 'lZRdO2wVxiR0YDg6ElcZD4uhXHhJNN49pCwxPLIHlQgo0pBJ8_TArbJaTkNp6NMKTLO8cPKPmhf1lQ', 'name': 'HULKSMASH1337', 'profileIconId': 3546, 'revisionDate': 1615616858000, 'summonerLevel': 217}
              precision    recall  f1-score   support

           0       0.85      0.79      0.81        14
           1       0.75      0.82      0.78        11

    accuracy                           0.80        25
   macro avg       0.80      0.80      0.80        25
weighted avg       0.80      0.80      0.80        25

The predicted outcome of the next game based on aggregate data over 5 games will be a loss
