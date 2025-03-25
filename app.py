import numpy as np
import pandas as pd
import streamlit as st 
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# import data.
df = pd.read_csv('data/athlete_events.csv')
region = pd.read_csv('data/noc_regions.csv')
fun_fact = [
    "The first ancient Olympic Games were held in 776 BC in Olympia, Greece.",
    "The Olympic Games were initially a religious festival in honor of Zeus, the king of the Greek gods.",
    "The modern Olympic Games were revived in 1896 by Pierre de Coubertin in Athens, Greece.",
    "The Olympic motto is 'Citius, Altius, Fortius', which means 'Faster, Higher, Stronger'.",
    "The first female Olympic competitor was Hélène de Pourtalès of Switzerland, who competed in the 1900 Paris Games.",
    "The 2020 Tokyo Olympics were postponed to 2021 due to the COVID-19 pandemic, marking the first time in modern history the Games were rescheduled.",
    "The Olympic flame is lit in Olympia, Greece, and then carried by runners in a relay to the host city.",
    "The United States has won the most Olympic medals of any country, with over 2,500 medals as of the 2020 Olympics.",
    "The Olympic Games have been canceled three times in history: in 1916, 1940, and 1944, due to World Wars I and II.",
    "The Olympic Games feature both Summer and Winter editions, with the Winter Games focusing on sports like skiing, ice skating, and ice hockey."
]


st.sidebar.title('Olympic Analysis')
st.sidebar.image('olympic_logo.png')

# preprocessing.
df = preprocessor.preprocess(df,region)

# selection sidebar.
user_input = st.sidebar.radio(
    'Select An Option :',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-wise Analysis')
)

if user_input == 'Medal Tally':
    
    # sidebar header.
    st.sidebar.header('Medal Tally')

    # list of years and countries (given as input to selectbox). 
    years, countries = helper.country_year_list(df)
    
    # getting year and country from user.
    selected_year = st.sidebar.selectbox('Select Years',years)
    selected_country = st.sidebar.selectbox('Select Country',countries)

    # tally according to input year and country.
    medal_year_country = helper.fetch_medal_tally(df,selected_year,selected_country)

    # header according to input.
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header('Overall Performances')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.header(selected_country + "'s Overall Performance")
    else:
        st.header(selected_country + " Performance in "+ str(selected_year))
    
    # display tally (dataframe).
    st.table(medal_year_country)

if user_input == 'Overall Analysis':

    # no. of editions, cities, sports etc.
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    countries = df['region'].unique().shape[0]

    st.title('Top Statistics.')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col4,col5,col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Countries')
        st.title(countries)
    with col6:
        st.header('Athletes')
        st.title(athletes)
        
    # chart of nations.
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time,x='Year',y='region')
    fig.update_layout(plot_bgcolor='aliceblue',yaxis_title='No. of Countries')
    st.title('Participating Nations Over the Years.')
    st.plotly_chart(fig)

    # chart of events.
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time,x='Year',y='Event')
    fig.update_layout(plot_bgcolor='aliceblue',yaxis_title='No. of Events')
    st.title('Events Over the Years.')
    st.plotly_chart(fig)

    # chart of athletes.
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time,x='Year',y='Name')
    fig.update_layout(plot_bgcolor='aliceblue',yaxis_title='No. of Athletes')
    st.title('Athletes Over the Years.')
    st.plotly_chart(fig)

    # heatmap for country's performance in sports yearwise.
    st.title('No. of Events Over Time.')
    fig,ax = plt.subplots(figsize=(35,35))
    x = df.drop_duplicates(['Year','Sport','Event'])
    sns.set(font_scale=2)
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    # Most successful Althletes.
    st.title('Most Successful Althletes.')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport :',sport_list) 

    x = helper.most_successful_sportwise(df,selected_sport)
    st.table(x)


if user_input == 'Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')

    # getting list of countries names.
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    # country selection by user.
    selected_country = st.sidebar.selectbox('Select a Country ',country_list) 

    # yearwise country's performance line plot.
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    fig.update_layout(plot_bgcolor='aliceblue')
    st.title(selected_country + ' Medal Tally over the Years.')
    st.plotly_chart(fig)

    # country's year-sports heatmap.
    pt = helper.country_event_heatmap(df,selected_country)
    if pt.size != 0:
        st.title(selected_country+"'s Performance in Various Sports.")
        fig,ax= plt.subplots(figsize=(35,35))
        sns.set(font_scale=2)
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)

    # top 15 athletes from selected country.
    st.title('Top Athletes from ' + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_input == 'Athlete-wise Analysis':
    
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    t1 = athlete_df['Age'].dropna()
    t2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    t3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    t4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # PDF of Age with medal counts.
    st.title('Age Distribution of Athletes.')
    fig = ff.create_distplot([t1,t2,t3,t4],['Overall Age','Gold Medal','Silver Medal','Bronze Medal'],show_hist=False,show_rug=False) 
    fig.update_layout(plot_bgcolor='aliceblue',autosize=False,width=1200,height=600,xaxis_title='Age',yaxis_title='Probability')
    st.plotly_chart(fig)

    # Age-wise distribution for popular sports.
    st.title('Sportswise Distribution of Age.')
    selected_medal = st.selectbox('Select Medal Type ',['Gold','Silver','Bronze'])
    famous_sports = ['Weightlifting','Volleyball','Table Tennis','Tennis','Swimming','Shooting','Judo','Gymnastics','Football','Cycling','Boxing','Basketball','Badminton','Athletics']
    x= [] 
    for sports in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sports]
        x.append(temp_df[temp_df['Medal'] == selected_medal]['Age'].dropna())

    fig = ff.create_distplot(x,famous_sports,show_hist=False,show_rug=False)
    fig.update_layout(plot_bgcolor='aliceblue',autosize=False,width=1200,height=600,xaxis_title='Age',yaxis_title='Probability')
    st.plotly_chart(fig)

    # men women performance comparision.
    st.title('Men and Women Participation Over the Years.')
    men_and_women = helper.men_women(df)
    fig = px.line(men_and_women,x='Year',y=['Men','Women'])
    fig.update_layout(plot_bgcolor='aliceblue')
    st.plotly_chart(fig)

# fun fact feature addtion.
random_int = np.random.randint(low=0, high=10)
st.sidebar.text('Did You Know : \n' + fun_fact[random_int])


