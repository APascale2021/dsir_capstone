# Campaign Finance Capstone Project
### Exploratory Data Analysis
#### **Encompasses all federal races from 1990-2016**
<br>

## Problem Statement:

To predict the amount of money that needs to be raised to win a congressional or senate race in the next election cycle, based on location and incumbency status.

### Methods:

First, I will need to figure out a large-scale storage solution to efficiently query all relevant data, and connect  databases on similar foreign keys (such as CandidateId). Then, I'll filter by Congressional and Senate campaigns and use clustering and principal component analysis to determine main groupings of campaigns -- I expect incumbency to be a primary factor.

After extensive analysis, I plan to use several linear regression models to predict the total amount of money to be raised. The final data product will be a Streamlit app where the user inputs:

- The type of race (Congressional/Senate)
- State
- District (if congressional)
- Political Party
- Incumbency

And the app will generate a prediction of:
- A sliding scale of total amount of money to be raised
    - shows percent chance of winning based on dollar amount
- Recommendations for
    - 10 Top individual donors for fundraising
    - 5 Top coporate PAC sponsors
    
### Source:
This dataset was downloaded from a Kaggle board: https://www.kaggle.com/jeegarmaru/campaign-contributions-19902016. However, the original data was scraped from https://www.opensecrets.org/open-data/bulk-data-documentation.