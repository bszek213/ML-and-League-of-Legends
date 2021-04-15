import helper
import time
start_time = time.perf_counter()
api,summoner_string = helper.import_data()
my_region = 'na1'
#Class Instantiation
riot = helper.RiotAccount(api,summoner_string,my_region)
#call methods
riot.summoner_data()
riot.get_match_count()
output_summoner_df = riot.get_match_data()
X = riot.Decision_Tree_Class(output_summoner_df)
riot.calculate_win_loss(output_summoner_df)
end_time = time.perf_counter()
print(f"Time to excute full code: {end_time-start_time:0.4f}")
riot.plot_data(X)
