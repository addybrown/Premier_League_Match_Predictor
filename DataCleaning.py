

#Main Imports
import pandas as pd
import numpy as np
from datetime import datetime


old_data=pd.read_csv(r'clean_data/clean_data.csv')

def result_mapper(result):
    if result=='H':
        return 2
    elif result=='A':
        return 1
    else:
        return 0

def result_search(dataframe, column_name, team_name): 
    
    dataframe_temp=dataframe['Date'][dataframe[column_name]==team_name]
    
    if len(dataframe_temp)>0:
        return np.argmax(dataframe_temp)
    else:
        return -1

def last_game_result(dataframe,team_name,date):
    
    dataframe_temp=dataframe[dataframe['Date']<date]
    
    x1=result_search(dataframe_temp,'HomeTeam',team_name)
    x2=result_search(dataframe_temp,'AwayTeam',team_name)
    
    #x1 means you were the home_team, x2 means you were the away_team
    
    if x1>x2:
        if dataframe_temp.loc[x1,'FTR']=='H':
            return 'W'
        elif dataframe_temp.loc[x1,'FTR']=='A':
            return 'L'
        else:
            return 'D'
    elif x1==x2:
        return -1
    else:
        if dataframe_temp.loc[x2,'FTR']=='A':
            return 'W'
        elif dataframe_temp.loc[x2,'FTR']=='H':
            return 'L'
        else:
            return 'D'

def check_form_value(dataframe,team_name,date):
    
    dataframe_temp=dataframe[dataframe['Date']<date]
    
    #print(dataframe_temp.head())

    x1=result_search(dataframe_temp,'HomeTeam',team_name)
    x2=result_search(dataframe_temp,'AwayTeam',team_name)
    
    if x1>x2:
        #Means Last Game was Home Game 
        if (dataframe_temp.loc[x1,'G1.H']==0 and dataframe_temp.loc[x1,'G2.H']==0 and dataframe_temp.loc[x1,'G3.H']==0):
            return 'G1.','Home',x1
        if (dataframe_temp.loc[x1,'G2.H']==0 and dataframe_temp.loc[x1,'G3.H']==0):
            return 'G2.','Home',x1
        elif (dataframe_temp.loc[x1,'G3.H']==0):
            return 'G3.','Home',x1
        else:
            return 'G3.','Home',x1
    elif x1<x2:
       #Means Last Game was Away Game 
        if (dataframe_temp.loc[x2,'G1.A']==0 and dataframe_temp.loc[x2,'G2.A']==0 and dataframe_temp.loc[x2,'G3.A']==0):
            return 'G1.','Away',x2
        if (dataframe_temp.loc[x2,'G2.A']==0 and dataframe_temp.loc[x2,'G3.A']==0):
            return 'G2.','Away',x2
        elif (dataframe_temp.loc[x2,'G3.A']==0):
            return 'G3.','Away',x2
        else:
            return 'G3.','Away',x2
        
    #only way is if both x1 and x2 are equal to -1
    else:
        return -1

def count_previous_games(dataframe,date,team_name):
    dataframe_temp=dataframe[(dataframe['HomeTeam']==team_name) | (dataframe['AwayTeam']==team_name)][dataframe['Date']<date]
    return len(dataframe_temp)

def count_prev_point(dataframe,date,team_name):
    dataframe_temp=dataframe[(dataframe['HomeTeam']==team_name) | (dataframe['AwayTeam']==team_name)][dataframe['Date']<date]
    dataframe_temp.index=range(0,len(dataframe_temp))
    #print(dataframe_temp)
    value=0
    for i in enumerate(dataframe_temp['Date']):
        #print(i[0])
        if dataframe_temp.loc[i[0],'FTR']=='H' and dataframe_temp.loc[i[0],'HomeTeam']==team_name:
            value=value+3
        elif dataframe_temp.loc[i[0],'FTR']=='A' and dataframe_temp.loc[i[0],'AwayTeam']==team_name:
            value= value+3
        elif dataframe_temp.loc[i[0],'FTR']=='D':
            value= value+1

    return value

def count_prev(dataframe,date,team_name,col):
    #print(col[0])
    data_temp1=dataframe[col[0]][(dataframe['HomeTeam']==team_name)][dataframe['Date']<date]
    data_temp2=dataframe[col[1]][(dataframe['AwayTeam']==team_name)][dataframe['Date']<date]
    return np.sum(data_temp1)+np.sum(data_temp2)
    data_temp1=dataframe['FTAG'][(dataframe['HomeTeam']==team_name)][dataframe['Date']<date]
    data_temp2=dataframe['FTHG'][(dataframe['AwayTeam']==team_name)][dataframe['Date']<date]
    return np.sum(data_temp1)+np.sum(data_temp2)

def DataCleaner(csv_name,prev_season_csv):

    #Importing Season CSV File
    df=pd.read_csv(csv_name)
    #print(df.head())
    df['Date'] = pd.to_datetime(df['Date'])

    #Making all default values equal to zero

    

    df['G1.H']=0
    df['G2.H']=0
    df['G3.H']=0
    df['G1.A']=0
    df['G2.A']=0
    df['G3.A']=0

    df = df.sort_values('Date', ascending=1)
    df.index=range(0,len(df))

    df['This_Year_LP_Home']=0
    df['Last_Year_LP_Home']=0
    df['This_Year_LP_Away']=0
    df['Last_Year_LP_Away']=0

    #Create Table For Standings:
    a=set(df['HomeTeam'])
    table=pd.DataFrame(index=range(0,len(a)))
    table['Team']=a
    table['Games']=0
    table['W']=0
    table['D']=0
    table['L']=0
    table['Points']=0
    #final_table=pd.DataFrame()
    #count=0
    #j=1
    last_table=pd.read_csv(prev_season_csv)
    last_table['Games']=38

    for i in enumerate(df.Date):
    
        home=df.loc[i[0],'HomeTeam']
        away=df.loc[i[0],'AwayTeam']
        
        df.loc[i[0],'This_Year_LP_Home']=np.argmax(table['Points'][table['Team']==home])+1
        df.loc[i[0],'This_Year_LP_Away']=np.argmax(table['Points'][table['Team']==away])+1
        
        #to ensure values do exist
        if (last_table['Points'][last_table['Team']==home].empty==False):
            
            df.loc[i[0],'Last_Year_LP_Home']=np.argmax(last_table['Points'][last_table['Team']==home])+1
        if (last_table['Points'][last_table['Team']==away].empty==False):
            df.loc[i[0],'Last_Year_LP_Away']=np.argmax(last_table['Points'][last_table['Team']==away])+1
        
        
        
        table.loc[table['Team']==home,'Games']=table.loc[table['Team']==home,'Games']+1
        table.loc[table['Team']==away,'Games']=table.loc[table['Team']==away,'Games']+1
        
        if df.loc[i[0],'FTR']=='H':
            
            table.loc[table['Team']==home,'Points']=table.loc[table['Team']==home,'Points']+3
            
            #Home and Away Loss Table
            table.loc[table['Team']==home,'W']=table.loc[table['Team']==home,'W']+1
            table.loc[table['Team']==away,'L']=table.loc[table['Team']==away,'L']+1
            
        elif df.loc[i[0],'FTR']=='A':
            
            table.loc[table['Team']==away,'Points']=table.loc[table['Team']==away,'Points']+3
            
            #Home and Away Loss Table
            table.loc[table['Team']==away,'W']=table.loc[table['Team']==away,'W']+1
            table.loc[table['Team']==home,'L']=table.loc[table['Team']==home,'L']+1
            
        else:
            table.loc[table['Team']==home,'Points']=table.loc[table['Team']==home,'Points']+1
            table.loc[table['Team']==away,'Points']=table.loc[table['Team']==away,'Points']+1
            
            #Home and Away Draw Table
            table.loc[table['Team']==away,'D']=table.loc[table['Team']==away,'D']+1
            table.loc[table['Team']==home,'D']=table.loc[table['Team']==home,'D']+1
            
        #resorts the table by who is the top team 
        table=table.sort_values(['Points'], ascending=False)
        table.index=range(0,len(table))
        
        table.head()

        if (i[0]+1<3800):
            #print(df.loc[i[0],'Date'].month,df.loc[i[0]-1,'Date'].month)
            if(df.loc[i[0],'Date'].month==5 and df.loc[i[0]+1,'Date'].month==8):
                #print('Season: '+str(j)+' Complete')
            # print(table.head())
                last_table=table
                final_table=final_table.append(table.loc[:19])
                
                table['Points']=0
                table['Games']=0
                table['W']=0
                table['L']=0
                table['D']=0
                
                j=j+1
        if (i[0]==3799):
            #print('Season: '+str(j)+' Complete')
        # print(table.head())
            final_table=final_table.append(table.loc[:19])

    for i in enumerate(df.Date):
        #print(i[0])
        #for home team
        
        #tells you if you won or lost 
        prev_game_result_home=last_game_result(df,df.loc[i[0],'HomeTeam'],i[1])
        
        #tells you where to put last result location
        prevform_loc_home=check_form_value(df,df.loc[i[0],'HomeTeam'],i[1])

        #for away team
        prev_game_result_away=last_game_result(df,df.loc[i[0],'AwayTeam'],i[1])
        prevform_loc_away=check_form_value(df,df.loc[i[0],'AwayTeam'],i[1])
        
        '''print(prev_game_result_home)
        print(prevform_loc_home)
        print(prev_game_result_away)
        print(prevform_loc_away)'''
        
        if (prev_game_result_home != -1 and prevform_loc_home!=-1):
            #currently hometeam
            if prevform_loc_home[1]=='Home':
                

                #copy over games 1,2,3 
                df.loc[i[0],'G1.H']=df.loc[prevform_loc_home[2],'G1.H']
                df.loc[i[0],'G2.H']=df.loc[prevform_loc_home[2],'G2.H']
                df.loc[i[0],'G3.H']=df.loc[prevform_loc_home[2],'G3.H']
                
                df.loc[i[0], prevform_loc_home[0] + 'H']= prev_game_result_home
                
                #print(prev_game_result_home)
            
            elif prevform_loc_home[1]=='Away':
                df.loc[i[0],'G1.H']=df.loc[prevform_loc_home[2],'G1.A']
                df.loc[i[0],'G2.H']=df.loc[prevform_loc_home[2],'G2.A']
                df.loc[i[0],'G3.H']=df.loc[prevform_loc_home[2],'G3.A']

                df.loc[i[0], prevform_loc_home[0] + 'H']= prev_game_result_home
            
        if (prev_game_result_away != -1 and prevform_loc_away!=-1):
            #df.loc[i[0], prevform_loc_away[0] + 'A']= prev_game_result_away
            
            if prevform_loc_away[1]=='Home':
                #copy over games 1,2,3 
                df.loc[i[0],'G1.A']=df.loc[prevform_loc_away[2],'G1.H']
                df.loc[i[0],'G2.A']=df.loc[prevform_loc_away[2],'G2.H']
                df.loc[i[0],'G3.A']=df.loc[prevform_loc_away[2],'G3.H']
                df.loc[i[0], prevform_loc_away[0] + 'A']= prev_game_result_away

            elif prevform_loc_away[1]=='Away':
                df.loc[i[0],'G1.A']=df.loc[prevform_loc_away[2],'G1.A']
                df.loc[i[0],'G2.A']=df.loc[prevform_loc_away[2],'G2.A']
                df.loc[i[0],'G3.A']=df.loc[prevform_loc_away[2],'G3.A']
                df.loc[i[0], prevform_loc_away[0] + 'A']= prev_game_result_away
                
    df['Home_Points']=0
    df['Away_Points']=0

    df['Home_Goals']=0
    df['Away_Goals']=0

    df['Home_Goals_Conceded']=0
    df['Away_Goals_Conceded']=0

    df['Home_Shots']=0
    df['Away_Shots']=0

    df['Home_Shots_Target']=0
    df['Away_Shots_Target']=0

    df['Home_Corners']=0
    df['Away_Corners']=0

    df['Home_Fouls']=0
    df['Away_Fouls']=0

    df['Home_Yellow']=0
    df['Away_Yellow']=0

    df['Home_Red']=0
    df['Away_Red']=0

    #Creates a list of team_names 
    team_names=list(set(df['HomeTeam']))
    #print(team_names)
    index_storage={}

    for i in team_names:

        #index_current=df[(df['HomeTeam']==i)|(df['AwayTeam']==i)].index.min()
        index_old=old_data[(old_data['HomeTeam']==i)|(old_data['AwayTeam']==i)].index.max()

        index_storage[i]=index_old
        #print(index_current)
        #print(index_old)

        #isHome=df.loc[index_current,'HomeTeam']==i

        #print(isHome)
        '''
        if isHome==True:
            df.loc[index_current,'Home_Points']=old_data.loc[index_old,'Home_Points']

            print('a: '+ str(df.loc[index_current,'Home_Points']))
            print('b: '+ str(old_data.loc[index_old,'Home_Points']))
            
            df.loc[index_current,'Home_Goals']=old_data.loc[index_old,'Home_Goals']
            df.loc[index_current,'Home_Avg_Shots']=old_data.loc[index_old,'Home_Avg_Shots']
            df.loc[index_current,'Home_Shots_Target']=old_data.loc[index_old,'Home_Shots_Target']
            df.loc[index_current,'Home_Corners']=old_data.loc[index_old,'Home_Corners']
            df.loc[index_current,'Home_Fouls']=old_data.loc[index_old,'Home_Fouls']
            df.loc[index_current,'Home_Yellow']=old_data.loc[index_old,'Home_Yellow']
            df.loc[index_current,'Home_Red']=old_data.loc[index_old,'Home_Red']
        else:
            df.loc[index_current,'Away_Points']=old_data.loc[index_old,'Away_Points']
            df.loc[index_current,'Away_Goals']=old_data.loc[index_old,'Away_Goals']
            df.loc[index_current,'Away_Avg_Shots']=old_data.loc[index_old,'Away_Avg_Shots']
            df.loc[index_current,'Away_Shots_Target']=old_data.loc[index_old,'Away_Shots_Target']
            df.loc[index_current,'Away_Corners']=old_data.loc[index_old,'Away_Corners']
            df.loc[index_current,'Away_Fouls']=old_data.loc[index_old,'Away_Fouls']
            df.loc[index_current,'Away_Yellow']=old_data.loc[index_old,'Away_Yellow']
            df.loc[index_current,'Away_Red']=old_data.loc[index_old,'Away_Red']
            '''
    print(df.head())

    stored_columns=['Home_Goals','Away_Goals','Home_Goals_Conceded','Away_Goals_Conceded',
                'Home_Shots','Away_Shots','Home_Shots_Target','Away_Shots_Target',
                'Home_Corners','Away_Corners','Home_Yellow','Away_Yellow','Home_Red','Away_Red']
    
    col_values=[['FTHG','FTAG'],['FTAG','FTHG'],['HS','AS'],['HST','AST'],['HC','AC'],['HY','AY'],['HR','AR']]

    for i in enumerate(df.Date):
        value_home=count_previous_games(df,df.loc[i[0],'Date'],df.loc[i[0],'HomeTeam'])
        value_away=count_previous_games(df,df.loc[i[0],'Date'],df.loc[i[0],'AwayTeam'])
        
        home_team=df.loc[i[0],'HomeTeam']
        away_team=df.loc[i[0],'AwayTeam']
        date=df.loc[i[0],'Date']

        if value_home==0:
            value_home=1
        if value_away==0:
            value_away=1
        
        if (value_home!=0  or value_away!=0):
            


            
            df.loc[i[0],'Home_Points']=(count_prev_point(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Points'])/value_home 
            df.loc[i[0],'Away_Points']=(count_prev_point(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Points'])/value_away
            
            for j in range(1,len(stored_columns),2):

                temp_val=int((j-1)/2)

                df.loc[i[0],stored_columns[j-1]]=(count_prev(df,date,home_team,col_values[temp_val])+old_data.loc[index_storage[home_team],stored_columns[j-1]])/value_home
            #a=stored_columns[i][0]
                df.loc[i[0],stored_columns[j]]=(count_prev(df,date,away_team,col_values[temp_val])+old_data.loc[index_storage[away_team],stored_columns[j]])/value_away


            '''
            df.loc[i[0],'Home_Goals']=(count_prev_goals(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Goals'])/value_home
            df.loc[i[0],'Away_Goals']=(count_prev_goals(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Goals'])/value_away
            
            df.loc[i[0],'Home_Goals_Conceded']=(count_prev_goals_conceded(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Goals_Conceded'])/value_home
            df.loc[i[0],'Away_Goals_Conceded']=(count_prev_goals_conceded(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Goals_Conceded'])/value_away

            df.loc[i[0],'Home_Avg_Shots']=(count_prev_shots(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Avg_Shots'])/value_home
            df.loc[i[0],'Away_Avg_Shots']=(count_prev_shots(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Avg_Shots'])/value_away

            df.loc[i[0],'Home_Shots_Target']=(count_prev_shots_target(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Shots_Target'])/value_home
            df.loc[i[0],'Away_Shots_Target']=(count_prev_shots_target(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Shots_Target'])/value_away

            df.loc[i[0],'Home_Corners']=(count_prev_corners(df,date,home_team)+old_data.loc[index_storage[home_team],'Home_Corners'])/value_home
            df.loc[i[0],'Away_Corners']=(count_prev_corners(df,date,away_team)+old_data.loc[index_storage[away_team],'Away_Corners'])/value_away

            #df.loc[i[0],'Home_Post']=count_prev_post(df,df.loc[i[0],'Date'],df.loc[i[0],'HomeTeam'])/value_home
            #df.loc[i[0],'Away_Post']=count_prev_post(df,df.loc[i[0],'Date'],df.loc[i[0],'AwayTeam'])/value_away

            #df.loc[i[0],'Home_Fouls']=(count_prev_fouls(df,date,home_team)+old_data[index_storage[home_team],'Home_Fouls'])/value_home
            #df.loc[i[0],'Away_Fouls']=(count_prev_fouls(df,date,away_team)+old_data[index_storage[away_team],'Away_Fouls'])/value_away

            #df.loc[i[0],'Home_Offisde']=count_prev_offside(df,df.loc[i[0],'Date'],df.loc[i[0],'HomeTeam'])/value_home
            #df.loc[i[0],'Away_Offisde']=count_prev_offside(df,df.loc[i[0],'Date'],df.loc[i[0],'AwayTeam'])/value_away

            #df.loc[i[0],'Home_Yellow']=(count_prev_yellows(df,date,home_team)+old_data[index_storage[home_team],'Home_Yellow'])/value_home
            #df.loc[i[0],'Away_Yellow']=(count_prev_yellows(df,date,away_team)+old_data[index_storage[away_team],'Away_Yellow'])/value_away

            df.loc[i[0],'Home_Red']=count_prev_reds(df,date,home_team)/value_home
            df.loc[i[0],'Away_Red']=count_prev_reds(df,date,away_team)/value_away

            #df.loc[i[0],'Home_FK_Concede']=count_prev_freekicks_concede(df,df.loc[i[0],'Date'],df.loc[i[0],'HomeTeam'])/value_home
            #df.loc[i[0],'Away_FK_Concede']=count_prev_freekicks_concede(df,df.loc[i[0],'Date'],df.loc[i[0],'Team'])/value_away
            '''
    df['Form_Rating_Home']=0
    df['Form_Rating_Away']=0

    for i in enumerate(df['Date']):
        value_home=0
        value_away=0
        for j in range(1,4):
            if df.loc[i[0],'G'+str(j)+'.H']=='D':
                value_home=value_home+1
            elif df.loc[i[0],'G'+str(j)+'.H']=='W':
                value_home=value_home+3
            if df.loc[i[0],'G'+str(j)+'.A']=='D':
                value_away=value_away+1
            elif df.loc[i[0],'G'+str(j)+'.A']=='W':
                value_away=value_away+3
                
        df.loc[i[0],'Form_Rating_Home']=value_home
        df.loc[i[0],'Form_Rating_Away']=value_away

        for i in range(1,4):
            df[['G0','G'+str(i)+'.H.D','G'+str(i)+'.H.L','G'+str(i)+'.H.W']]=pd.get_dummies(df['G'+str(i)+'.H'])
            df[['G0','G'+str(i)+'.A.D','G'+str(i)+'.A.L','G'+str(i)+'.A.W']]=pd.get_dummies(df['G'+str(i)+'.A'])


    df['Home_GD']=df['Home_Goals']-df['Home_Goals_Conceded']
    df['Away_GD']=df['Away_Goals']-df['Away_Goals_Conceded']
    df['FTR.numerical']=df['FTR'].apply(result_mapper)

    clean_data=df[['HomeTeam','AwayTeam','Date','Home_Points', 'Away_Points', 'Home_GD', 'Away_GD','G1.H.D',
       'G1.H.L', 'G1.H.W', 'G1.A.D', 'G1.A.L', 'G1.A.W', 'G2.H.D', 'G2.H.L',
       'G2.H.W', 'G2.A.D', 'G2.A.L', 'G2.A.W', 'G3.H.D', 'G3.H.L', 'G3.H.W',
       'G3.A.D', 'G3.A.L', 'G3.A.W', 'Home_Shots', 'Away_Shots','Home_Red', 'Away_Red','This_Year_LP_Home',
       'Last_Year_LP_Home', 'This_Year_LP_Away', 'Last_Year_LP_Away','FTR.numerical']]
    
    '''
    clean_data=df[['Home_Points','Away_Points','Date', 'HomeTeam', 'AwayTeam', 'Home_Goals','Away_Goals', 'Home_Goals_Conceded','Away_Goals_Conceded','Form_Rating_Home',
        'Form_Rating_Away', 'Home_Shots', 'Away_Shots',
        'Home_Shots_Target', 'Away_Shots_Target', 'Home_Corners',
        'Away_Corners', 'Home_Fouls', 'Away_Fouls', 'Home_Yellow',
        'Away_Yellow', 'Home_Red', 'Away_Red','G1.H','G2.H','G3.H','G1.A','G2.A','G3.A','This_Year_LP_Home','Last_Year_LP_Home',
                'This_Year_LP_Away','Last_Year_LP_Away','FTR']]
    '''

    return clean_data








