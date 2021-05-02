import streamlit as st
import pickle

import numpy as np
import pandas as pd

global senate_rank
global house_rank
global state_list
global state_codes

st.title('Campaign Finance')
st.header('Fundraising Model')
st.subheader('Congressional and Senate Campaigns 2000-2014')
st.text('Please input your data below:')

sen_states = pd.read_csv('senate_rankings.csv')
all_districts = pd.read_csv('district_rankings.csv')
usps = pd.read_csv('state_abbrev.csv')

def df_to_dict(df):
    new_dict = {}

    for i, key in enumerate(df.iloc[:,0]):
        new_dict[key] = df.iloc[:,1][i]

    return new_dict

senate_rank = df_to_dict(sen_states)
house_rank = df_to_dict(all_districts)
state_codes = df_to_dict(usps)
state_list = []

def get_districts(state, rankings):
    districts = [key for key in rankings.keys() if key.startswith(state)]
    return sorted(districts)

#try:
#        st.text('blank')
#except:
#    pass

with st.form(key='my_form'):
    text_input = st.text_input(label='Enter your name')
    political_party = st.radio('Political Party', ['Republican','Democrat'])
    campaign_type = st.radio('Type of Campaign', ['Senate', 'Congressional'])
    state = st.selectbox('Select', list(state_codes.keys()))

    # cache state into the file
    state_list.append(state)
    with open('states.pk', 'wb') as file:
        pickle.dump(state_list, file)

    if campaign_type == 'Congressional':
        with open('states.pk', 'rb') as file:
            cached_states = pickle.load(file)
            dist_list = get_districts(state_codes[cached_states.pop()], house_rank)
        district = st.selectbox('Select', dist_list)

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if campaign_type == 'Senate':
        st.write(f'{text_input} is working on a {political_party} {campaign_type} campaign in {state}')
    elif campaign_type == 'Congressional':
        st.write(f'{text_input} is working on a {political_party} {campaign_type} campaign in {district}')
