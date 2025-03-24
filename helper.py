import numpy as np

def medal_tally(df):

    # fixing wrong medal counts by removing same team players.
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    # getting medal counts on the basis of region.
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    # adding extra column of total medal count.
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):

    # list of years.
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    # list of countries.
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'Overall')

    return years,countries

def fetch_medal_tally(input_df,year,country):
    
    # correction for team medal countings.
    medal_df = input_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag = 0 
    
    # Overall Tally.
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    
    # Country's Overall tally (year-wise medals of country).
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    
    # tally in a specific year.
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    # specific country in specifc year.
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
        
        
    if flag == 0:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    else:
        # special case : year-wise medals of country.
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x.index += 1

    return x



def data_over_time(df,col):
    data_over = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over.rename(columns={'count': col},inplace=True)
    return data_over

def yearwise_medal_tally(df,country):
    # remove entries with no medals.
    temp_df = df.dropna(subset=['Medal'])

    # correction for team medal countings.
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    # filter country.
    country_df = temp_df[temp_df['region'] == country]
    
    # yearwise no. of medals.
    country_df = country_df.groupby('Year').count()['Medal'].reset_index()

    return country_df

def country_event_heatmap(df,country):
    # remove entries with no medals.
    temp_df = df.dropna(subset=['Medal'])

    # correction for team medal countings.
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    # filter country.
    country_df = temp_df[temp_df['region'] == country]

    # pivot table for selected country.
    pt = country_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)

    return pt

def most_successful_sportwise(df,sport):
    # remove entries with no medals.
    temp_df = df.dropna(subset=['Medal'])
    
    # filter sports.
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    # information of top 15 athletes.
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,on='Name',how='left')[['Name','count','Sport','region']]

    # remove duplicates and old index, add new index starting from 1.
    x = x.drop_duplicates('Name').reset_index(drop=True)
    x.index += 1

    return x

def most_successful_countrywise(df,country):
    # remove entries with no medals.
    temp_df = df.dropna(subset=['Medal'])
    
    # filter country.
    temp_df = temp_df[temp_df['region'] == country]
    
    # information of top 15 players from selected country.
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,on='Name',how='left')[['Name','count','Sport']]

    # remove duplicates and old index, add new index starting from 1.
    x = x.drop_duplicates('Name').reset_index(drop=True)
    x.index += 1

    return x

def men_women(df):

    athlete_df = df.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    
    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Men','Name_y':'Women'},inplace=True)
    final.fillna(0,inplace=True)

    return final



    
    


