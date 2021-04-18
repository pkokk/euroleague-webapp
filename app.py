import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Euroleague Player Stats')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2001,2022))))

st.markdown("""
Adaptation of : [Data Professor Basketball App](https://github.com/dataprofessor/basketball-heroku).
""")


# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/international/euroleague/"+ str(year) +"_totals.html"
    html = pd.read_html(url)
    df = html[0].fillna(0)
    return df

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Team.unique())
sorted_stats = sorted(playerstats.columns)
selected_stat = st.sidebar.selectbox('Stat Category',sorted_stats)
select_top_n = st.sidebar.slider('Show Top N Leaders', 1,30, value = 20)
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)


# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team))].set_index('Player')
df_selected_team = df_selected_team[[selected_stat]]

st.header('Display Leaders in '+selected_stat)

st.set_option('deprecation.showPyplotGlobalUse', False)
ax = df_selected_team.sort_values(by=selected_stat).tail(select_top_n).plot.barh(y=selected_stat)
st.pyplot()