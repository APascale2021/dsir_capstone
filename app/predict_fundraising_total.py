import streamlit as st
import pickle
import form_input_convert
import numpy as np
import pandas as pd

global house_rank
global state_list
global features_list
global state_codes

st.title('Campaign Finance Capstone')
st.subheader('Congressional and Senate Campaigns 2000-2014')
st.text('Please input your data below:')

usps = pd.read_csv('state_abbrev.csv')
all_districts = pd.read_csv('district_rankings.csv')

def df_to_dict(df):
    new_dict = {}

    for i, key in enumerate(df.iloc[:,0]):
        new_dict[key] = df.iloc[:,1][i]

    return new_dict

state_codes = df_to_dict(usps)
house_rank = df_to_dict(all_districts)
state_list = []
features_list = []

def get_districts(state, rankings):
    districts = [key for key in rankings.keys() if key.startswith(state)]
    return sorted(districts)

with st.form(key='my_form'):
    name = st.text_input(label='Enter your name')
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

st.write('\n')

if submit_button:
    if campaign_type == 'Senate':
        st.subheader(f'{name} is working on a {political_party} {campaign_type} campaign in {state}')
        sen_features = form_input_convert.convert_data(2014, campaign_type, political_party, state, None)
        features_list.append(sen_features)
        with open('features_list.pk', 'wb') as file:
            pickle.dump(features_list, file)

        st.write('Here are the features that went into the model:')
        st.write(form_input_convert.list_to_df(sen_features))
        sen_total = form_input_convert.get_prediction(sen_features)[0]
        st.write('********')
        st.write(f'In order to win, {name} needs to raise the following:')
        st.header(form_input_convert.to_millions(sen_total))
    elif campaign_type == 'Congressional':
        st.subheader(f'{name} is working on a {political_party} {campaign_type} campaign in {district}')
        congr_features = form_input_convert.convert_data(2010, campaign_type, political_party, state, district)
        features_list.append(congr_features)
        with open('features_list.pk', 'wb') as file:
                pickle.dump(features_list, file)

        st.write('Here are the features that went into the model:')
        st.write(form_input_convert.list_to_df(congr_features))
        congr_total = form_input_convert.get_prediction(congr_features)[0]*.45
        st.write('********')
        st.write(f'In order to win, {name} needs to raise the following:')
        st.header(form_input_convert.to_millions(congr_total))

funds = st.slider('How many millions do you think you can raise?', min_value=.5, max_value=15.0, step=.2)
with open('features_list.pk', 'rb') as file:
        saved_features = pickle.load(file)
cached_features = saved_features.pop()
#st.write('Here are the features that went into the model:')
st.write(form_input_convert.list_to_df(cached_features + [funds]))

# Adjusted funds if senate race
if cached_features[1]==1:
    adj = .5
else:
    adj = 1
final_prediction = form_input_convert.predict_win(cached_features + [funds*adj])

st.subheader(f"If you can raise {form_input_convert.to_millions(funds)} dollars")
st.header(f'You have a {round(final_prediction, 2)}% chance of winning.')
