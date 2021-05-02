import pickle
import numpy as np
import pandas as pd

# Convert pandas DataFrame to a Dictionary
def df_to_dict(df):
    new_dict = {}

    for i, key in enumerate(df.iloc[:,0]):
        new_dict[key] = df.iloc[:,1][i]

    return new_dict

# Convert full-word state to 2-letter postal abbreviation
def get_state_code(state):
    usps = pd.read_csv('state_abbrev.csv')
    state_codes = df_to_dict(usps)
    return state_codes[state]

# Collect form inputs and return a list of features
def convert_data(cycle, campaign_type, political_party, state, district):
    cycle = (cycle-2000)/2
    sen = 0
    dem = 0
    repub = 0
    comp_score = 0

    if campaign_type=='Senate':
        sen = 1

    if political_party=='Democrat':
        dem = 1
    elif political_party=='Republican':
        repub = 1
    else:
        dem = 0
        repub = 0

    if campaign_type=='Senate':
        comp_score = get_comp_score(get_state_code(state))
    else:
        comp_score = get_comp_score(district)

    return [cycle, sen, dem, repub, comp_score]

# Return the weighted average for a state or district
def get_comp_score(territory):
    sen_states = pd.read_csv('senate_rankings.csv')
    all_districts = pd.read_csv('district_rankings.csv')

    senate_rank = df_to_dict(sen_states)
    house_rank = df_to_dict(all_districts)

    if len(territory)==2:
        return senate_rank[territory]
    else:
        return house_rank[territory]
