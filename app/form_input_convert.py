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

# Convert a list of features into a DataFrame
def list_to_df(test_data):
    df = pd.DataFrame(data=test_data).T
    if len(test_data)==5:
        df.columns=['cycle', 'sen', 'dem', 'repub', 'comp_score']
    elif len(test_data)==6:
        df.columns=['cycle', 'sen', 'dem', 'repub', 'comp_score', 'funds']
    return df

# Get predicted fundraising total from a list of features
def get_prediction(features_list):
    with open('lr_model.pk', 'rb') as file:
        saved_model = pickle.load(file)

    new_df = list_to_df(features_list)

    return saved_model.predict(new_df)

def predict_win(features_list):
    with open('lg_model.pk', 'rb') as file:
        saved_model_2 = pickle.load(file)

    new_df2 = list_to_df(features_list)

    percent_win = saved_model_2.predict_proba(new_df2).ravel()

    return percent_win[1]*100

# Return a formatted number in millions per decimal
def to_millions(n):
    total = n*1_000_000
    total = round(total, 2)
    num = str(total)
    i = num.index('.')
    decimal_pt = num[i+1:]

    if len(num.split('.')[0]) <= 6:
        if decimal_pt == '0':
            return '$'+num[:3]+','+num[3:i]
        else:
            return '$'+num[:3]+','+num[3:]
    elif len(num.split('.')[0]) == 7:
        if decimal_pt == '0':
            return '$'+num[:1]+','+num[1:4]+','+num[4:i]
        else:
            return '$'+num[:1]+','+num[1:4]+','+num[4:]
    else:
        if decimal_pt == '0':
            return '$'+num[:2]+','+num[2:5]+','+num[5:i]
        else:
            return '$'+num[:2]+','+num[2:5]+','+num[5:]
