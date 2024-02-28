import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

sns.set(style='dark')

def create_users_counts_df(day_df):
    users_counts_df = day_df.groupby('weekday')[['registered', 'casual', 'cnt']].sum().reset_index()
    users_counts_df = pd.melt(
        day_df, id_vars=['weekday'], 
        value_vars=['registered', 'casual'], 
        var_name='user_type', 
        value_name='count')
    return users_counts_df

def create_season_counts_df(day_df):
    season_counts_df = day_df.groupby(by='season').agg({
        'cnt': 'sum',
        'registered': 'sum',
        'casual': 'sum'
    }).reset_index()
    
    return season_counts_df

def create_monthly_counts_df(day_df):
    monthly_counts_df = day_df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })
    monthly_counts_df['mnth'] = monthly_counts_df.index.strftime('%B')
    monthly_counts_df['yr'] = monthly_counts_df.index.strftime('%Y')
    monthly_counts_df = monthly_counts_df.reset_index(drop=True)
    return monthly_counts_df

def create_weather_counts_df(day_df):
    weather_counts_df = day_df.groupby('weathersit').agg({
        'cnt': 'sum'
    }).reset_index()
    return weather_counts_df

day_df = pd.read_csv("https://raw.githubusercontent.com/putrishanty/data-analysis-project/main/dashboard/day_clean.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.sidebar.header("Filter:")
    
    start_date, end_date = st.date_input(
        label="Time Range", 
        min_value=min_date, 
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

users_counts_df = create_users_counts_df(main_df)
season_counts_df = create_season_counts_df(main_df)
monthly_counts_df = create_monthly_counts_df(main_df)
weather_counts_df = create_weather_counts_df(main_df)

st.header('Data Analysis Project: Bike Sharing :sparkles:')
st.subheader('Bike Sharing Counts')

col1, col2, col3 = st.columns(3)

with col1:
    total_counts = main_df['cnt'].sum()
    st.metric("Total Counts", value=total_counts)
with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Total Registered Users", value=total_registered)
with col3:
    total_casual = main_df['casual'].sum()
    st.metric("Total Casual Users", value=total_casual)


st.subheader('The Overall Trends In Two Years Period')

fig = px.line(monthly_counts_df, x="mnth", y="cnt", color="yr")
fig.update_layout(xaxis_title='Month', yaxis_title='Counts')

st.plotly_chart(fig, use_container_width=True)

with st.expander("Conclusion"):
    st.write(
        """The overall trend in bike sharing counts over the two-year period 
        suggests a growing popularity of bike sharing, evident through both 
        seasonal fluctuations and a consistent upward trajectory year-over-year.
        """
    )


st.subheader('The Distribution Between Weekdays, Workingdays and Holidays')

fig1 = px.bar(day_df, x="weekday", y="cnt", color="weekday", title='Weekdays', category_orders={"weekday": day_order})
fig2 = px.bar(day_df, x="workingday", y="cnt", color="workingday", title='Working Days')
fig3 = px.bar(day_df, x="holiday", y="cnt", color="holiday", title='Holidays')

for fig in [fig1, fig2, fig3]:
    fig.update_layout(xaxis_title='', yaxis_title='Counts', showlegend=False)

st.plotly_chart(fig1, use_container_width=True)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig2, use_container_width=True)
with right_column:
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("Conclusion"):
    st.write(
        """The distribution of bike sharing varies notably between weekdays, 
        working days, and holidays. Weekdays, particularly Fridays, witness 
        the highest rental volumes, indicating commuter usage. Working days 
        generally have lower ridership, with weekends experiencing the least 
        activity. Holidays show increased rentals, signaling a shift towards 
        leisure-oriented bike usage.
        """
    )


st.subheader('The Impact of Weather Conditions')

fig = px.bar(weather_counts_df, x="weathersit", y="cnt", color="weathersit")

fig.update_layout(xaxis_title='Weather', yaxis_title='Counts', showlegend=False)

st.plotly_chart(fig)

with st.expander("Conclusion"):
    st.write(
        """Weather conditions have a notable impact on bike sharing, with 
        clear/partly cloudy days consistently fostering higher ridership 
        across all seasons. Conversely, light snow/rain conditions correlate 
        with decreased rentals, particularly in winter. The effect of 
        misty/cloudy days is more variable, influenced by seasonal dynamics 
        and specific weather patterns.
        """
    )


st.subheader('Proportion from Registered and Casual Users')

fig = px.bar(users_counts_df, x='weekday', y='count', color='user_type', barmode='group')

fig.update_layout(xaxis_title='Weekdays', yaxis_title='Counts', showlegend=False)

st.plotly_chart(fig)

with st.expander("Conclusion"):
    st.write(
        """Registered users contribute a larger proportion of daily bike 
        sharing counts compared to casual users, indicating their dominant 
        role in utilizing the bike sharing service on a regular basis. 
        Despite this, casual users still form a significant portion of the 
        overall bike-sharing activity, highlighting the diversity in user 
        demographics and usage patterns.
        """
    )


st.subheader('The Impact of Weather Variables')

fig1 = px.scatter(day_df, x='temp', y='cnt', title='Temperature vs. Bike Sharing Counts')
fig2 = px.scatter(day_df, x='atemp', y='cnt', title='Apparent Temperature vs. Bike Sharing Counts')
fig3 = px.scatter(day_df, x='hum', y='cnt', title='Humidity vs. Bike Sharing Counts')
fig4 = px.scatter(day_df, x='windspeed', y='cnt', title='Windspeed vs. Bike Sharing Counts')

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)

with st.expander("Conclusion"):
    st.write(
        """Temperature and apparent temperature show a moderate positive 
        correlation with bike sharing counts, suggesting increased activity 
        with higher temperatures. Humidity and windspeed have less clear 
        relationships with bike sharing counts, indicating their impact may 
        be minimal. Overall, temperature and apparent temperature seem to 
        have a more noticeable impact on bike sharing compared to humidity 
        and windspeed
        """
    )

st.caption('Copyright (c) Putri Shanty 2024')
