# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:32:54 2021

@author: Jonathan Flanagan (x18143890)
"""
# imports
import pandas as pd
import Scraper as scrp
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

"""
    Get the Figther, Fighter Additional Details, Event Details, 
    Event Fight Details as DataFrames for our 3 Datasets
    
    Main Dataset is the details from each event 
    and complimentary data sets are the fighter, 
    and fight details datasets.
    
    Datasets will be:
        
    Fighter Details
    - The Fighter Details will be have the DOB column from the Fighter Additional Details
      Dataframe appended to the it during the Normalization process.
    
    Event Details
    - Event details will be expanded out creating new attributes out of the existing ones
      from the DataFrame, this will be to preserve the rules of First Normal form where 
      each column has only one piece of data and is a consistent datatype for the attribute
      
    Fight Details
    - The fight details will be expanded to create new attributes in the same way as the
      the Event Details.
    
    In total 10,658 unique url's are scraped in the process and can take several 
    hours to complete depending on computer hardware and internet bandwidth. 
    
    This process is soley for normalizing the data and any cleaning/dealing with missing/null
    data or creating calcuted or secondary attributes will be done in a seperate stage of the process
    
    For my personal computer hardware / internet bandwidth combination it took:
    4hrs to scrape and retrieve all datasets.
"""

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

"""
    Get the fighter data and normalize the data so that each attribute contains one
    piece of information and that the information is consistent. Dealing with empty and 
    Null values will take place in a different step to preparing the data.
"""
def get_fighters():
    
    # Get the Fighter Basic Information
    fighters_df = scrp.get_fighters()
    
    # Get additional Fighter details
    fighter_details_df = scrp.get_further_fighter_details()
    
    # Add a blank DOB column to the end of the DataFrame
    columns = len(fighters_df.columns)
    fighters_df.insert(columns,'DOB','')
    
    # Append DOB info to the fighters Dataframe
    for i in range(len(fighters_df)):
        fighters_df.loc[i, 'DOB'] = fighter_details_df['DOB'].loc[i]
        
    
    # remove characters in Wt. Column 
    fighters_df['Wt.'] = fighters_df['Wt.'].str.replace('lbs.', '', regex=False)
    fighters_df['Wt.'] = fighters_df['Wt.'].apply(pd.to_numeric, errors='coerce')

    # remove charcters from Reach column
    fighters_df['Reach'] = fighters_df['Reach'].str.replace('"','', regex=False)
    fighters_df['Reach'] = fighters_df['Reach'].str.replace('--','', regex=False)
    fighters_df['Reach'] = fighters_df['Reach'].apply(pd.to_numeric, errors='coerce')

    # serperate out the Heigth Column by feet and inches and remove unwanted characters
    fighters_df[['Height:Ft', 'Height:Inch']] = fighters_df['Ht.'].str.split("'", expand=True)
    fighters_df['Height:Ft'] = fighters_df['Height:Ft'].str.replace('--','', regex=False)
    # Convert the Feet to inches
    fighters_df['Height:Ft'] = fighters_df['Height:Ft'].apply(pd.to_numeric, errors='coerce')
    fighters_df['Height:Ft'] = fighters_df['Height:Ft'] * 12
    # Convert inches to numeric
    fighters_df['Height:Inch'] = fighters_df['Height:Inch'].str.replace('"','', regex=False)
    fighters_df['Height:Inch'] = fighters_df['Height:Inch'].apply(pd.to_numeric, errors='coerce')
    # Convert put the Height back together as inches
    fighters_df['Height'] = (fighters_df['Height:Ft'] + fighters_df['Height:Inch'])
    
    # Strip DOB: from cells and re-arrange the date to useable format
    fighters_df['DOB'] = fighters_df['DOB'].str.replace('DOB:', '', regex=False)
    fighters_df[['DOB:Month', 'DOB:Year']] = fighters_df['DOB'].str.split(',', expand=True)
    fighters_df['DOB:Day'] = fighters_df['DOB:Month'].str.extract('(\d+)', expand=False)
    fighters_df['DOB:Month'] = fighters_df['DOB:Month'].str.extract('(^[a-z,A-Z]*)', expand=False)
    fighters_df['DOB'] = fighters_df['DOB:Day']+'-'+fighters_df['DOB:Month']+'-'+fighters_df['DOB:Year']
    fighters_df['DOB'] = pd.to_datetime(fighters_df['DOB'])
    
    # Make sure the W, L, D columns are as type int
    fighters_df['W'] = fighters_df['W'].astype(int)
    fighters_df['L'] = fighters_df['L'].astype(int)
    fighters_df['D'] = fighters_df['D'].astype(int)


    # Rename Columns
    fighters_df.rename(columns={'First':'First Name', 'Last': 'Last Name', 
                                'Wt.': 'Weight', 'W':'Wins','L':'Losses', 'D':'Draws'}, inplace=True)
    
    # Reindex the Columns wanted
    fighters_df = fighters_df.reindex(columns=['First Name',
                                               'Last Name',
                                               'Nickname',
                                               'Height',
                                               'Weight',
                                               'Reach',
                                               'Stance',
                                               'Wins',
                                               'Losses',
                                               'Draws',
                                               'DOB'])

    return fighters_df

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# Get the figthers information and export to CSV
# =============================================================================
# fighters_df = get_fighters()
# fighters_df.info()
# fighters_df.dtypes
# print(fighters_df)
# fighters_df.to_csv('../data/fighters.csv', index=False)
# 
# =============================================================================
#------------------------------------------------------------------------------------------------------------------------

# Get the events and their details
#event_details_df = scrp.get_event_details()

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# Get the details of each fight at each event
def get_fights():

    #fight_details_df = scrp.get_event_fight_details()
    file =('../data/fights.csv')
    fight_details_df = pd.read_csv(file)
    
    #--------------------------------------------------------------------------------------------------------------------
   
    # Split out columns into 2 by double space delimiter, to represent one for each fighter
    def split(frame, y):
        frame[[y+' F_1', y+' F_2']] = frame[y].str.split('  ', expand=True)
    
        return frame[y+' F_1'], frame[y+' F_2']
    
    #--------------------------------------------------------------------------------------------
           
    # Get the knockdowns for each fighter
    knock_downs_split = split(fight_details_df.copy(), 'KD')
    fight_details_df['KD F_1'] = knock_downs_split[0].apply(pd.to_numeric, errors='coerce')
    fight_details_df['KD F_2'] = knock_downs_split[1].apply(pd.to_numeric, errors='coerce')
    
    # Get the submission attempts by each fighter
    submissions_split = split(fight_details_df.copy(), 'Sub. att')
    fight_details_df['Sub. att F_1'] = submissions_split[0].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sub. att F_2'] = submissions_split[1].apply(pd.to_numeric, errors='coerce')
    
    # Get the reversals for each fighter
    reversals_split = split(fight_details_df.copy(), 'Rev.')
    fight_details_df['Rev. F_1'] = reversals_split[0].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Rev. F_2'] = reversals_split[1].apply(pd.to_numeric, errors='coerce')

    #----------------------------------------------------------------------------------------------

    # Split out the Sig. str. column into 2 to represent one for each fighter
    def significant_strikes(frame, y):
        frame[y] = frame[y].str.replace(' of ', 'of', regex=False)
        frame[[y+' F_1', y+' F_2']] = frame[y].str.split('  ', expand=True)
        frame[[y+' landed F_1', y+' thrown F_1']] = frame[y+' F_1'].str.split('of', expand=True)
        frame[[y+' landed F_2', y+' thrown F_2']] = frame[y+' F_2'].str.split('of', expand=True)
        
        return frame[y+' landed F_1'],frame[y+' thrown F_1'],frame[y+' landed F_2'],frame[y+' thrown F_2']
        
    # Get the significant strikes for each fighter
    sig_strikes = significant_strikes(fight_details_df.copy(), 'Sig. str.')
    fight_details_df['Sig. str. landed F_1'] = sig_strikes[0].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sig. str. thrown F_1'] = sig_strikes[1].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sig. str. landed F_2'] = sig_strikes[2].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sig. str. thrown F_2'] = sig_strikes[3].apply(pd.to_numeric, errors='coerce')
    
    #--------------------------------------------------------------------------------------------------------------------
    
    # Split out Sig. str. % column into 2 to represent one for each fighter
    fight_details_df[['Sig. str. % F_1', 'Sig. str. % F_2']]=fight_details_df['Sig. str. %'].str.split('  ', expand=True)
    fight_details_df['Sig. str. % F_1'] = fight_details_df['Sig. str. % F_1'].str.replace('%', '', regex=False)
    fight_details_df['Sig. str. % F_1'] = fight_details_df['Sig. str. % F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sig. str. % F_1'] = fight_details_df['Sig. str. % F_1'] / 100
    fight_details_df['Sig. str. % F_2'] = fight_details_df['Sig. str. % F_2'].str.replace('%', '', regex=False)
    fight_details_df['Sig. str. % F_2'] = fight_details_df['Sig. str. % F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Sig. str. % F_2'] = fight_details_df['Sig. str. % F_2'] / 100
    fight_details_df = fight_details_df.drop(['Sig. str. %'], axis=1)
    
    #--------------------------------------------------------------------------------------------------------------------

    # Split out the Total str. column into 2 to represent one for ach fighter
    fight_details_df['Total str.']=fight_details_df['Total str.'].str.replace(' of ', 'of', regex=False)
    fight_details_df[['Total str. F_1', 'Total str. F_2']]=fight_details_df['Total str.'].str.split('  ', expand=True)
    fight_details_df[['Total str. landed F_1', 'Total str. thrown F_1']] = fight_details_df['Total str. F_1'].str.split('of', expand=True)
    fight_details_df['Total str. landed F_1'] = fight_details_df['Total str. landed F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Total str. thrown F_1'] = fight_details_df['Total str. thrown F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df[['Total str. landed F_2', 'Total str. thrown F_2']] = fight_details_df['Total str. F_2'].str.split('of', expand=True)
    fight_details_df['Total str. landed F_2'] = fight_details_df['Total str. landed F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Total str. thrown F_2'] = fight_details_df['Total str. thrown F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df = fight_details_df.drop(['Total str.','Total str. F_1','Total str. F_2'], axis=1)


    # Split out the TD column into 2 to represent one for each fighter
    fight_details_df['Td'] =  fight_details_df['Td'].str.replace(' of ', 'of', regex=False)
    fight_details_df[['Td F_1', 'Td F_2']] = fight_details_df['Td'].str.split('  ', expand=True)
    fight_details_df[['Td completed F_1', 'Td attempted F_1']]=fight_details_df['Td F_1'].str.split('of', expand=True)
    fight_details_df['Td completed F_1'] = fight_details_df['Td completed F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Td attempted F_1'] = fight_details_df['Td attempted F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df[['Td completed F_2', 'Td attempted F_2']]=fight_details_df['Td F_2'].str.split('of', expand=True)
    fight_details_df['Td completed F_2'] = fight_details_df['Td completed F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Td attempted F_2'] = fight_details_df['Td attempted F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df = fight_details_df.drop(['Td','Td F_1', 'Td F_2'], axis=1)

    #--------------------------------------------------------------------------------------------------------------------

    # Split out Td % column into 2 to represent one for each fighter
    fight_details_df[['Td % F_1', 'Td % F_2']] = fight_details_df['Td %'].str.split('  ', expand=True)
    fight_details_df['Td % F_1'] = fight_details_df['Td % F_1'].str.replace('%', '', regex=False).replace('---', '', regex=False)
    fight_details_df['Td % F_1'] = fight_details_df['Td % F_1'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Td % F_1'] = fight_details_df['Td % F_1'] / 100
    fight_details_df['Td % F_2'] = fight_details_df['Td % F_2'].str.replace('%', '', regex=False).replace('---', '', regex=False)
    fight_details_df['Td % F_2'] = fight_details_df['Td % F_2'].apply(pd.to_numeric, errors='coerce')
    fight_details_df['Td % F_2'] = fight_details_df['Td % F_2'] / 100
    fight_details_df = fight_details_df.drop(['Td %'], axis=1)
    
    #------------------------------------------------------------------------------------------------
    
    # Get the control times for each fighter
    control_split = split(fight_details_df.copy(), 'Ctrl')
    c_split_F_1 = control_split[0]
    c_split_F_1 = c_split_F_1.to_frame()
    c_split_F_2 = control_split[1]
    c_split_F_2 = c_split_F_2.to_frame()

    # Convert the control times in seconds for better calculations
    def control_times(frame, x, y):
        frame[[x+'_min '+y, x+'_sec '+y]] = frame[x+' '+y].str.split(':', expand=True)
        frame[x+'_min '+y] = frame[x+'_min '+y].apply(pd.to_numeric, errors='coerce')
        frame[x+'_min '+y] = frame[x+'_min '+y]*60
        frame[x+'_sec '+y] = frame[x+'_sec '+y].apply(pd.to_numeric, errors='coerce')
        frame[x+' '+y] = frame[x+'_min '+y] + frame[x+'_sec '+y]
        
        return frame[x+' '+y]

    # Get the converted control times
    control_times_f1 = control_times(c_split_F_1, 'Ctrl', 'F_1')
    control_times_f2 = control_times(c_split_F_2, 'Ctrl', 'F_2')
    fight_details_df['Ctrl F_1'] = control_times_f1
    fight_details_df['Ctrl F_2'] = control_times_f2
    
    #-------------------------------------------------------------------------------------------------
    
    # Split out the needed columns from strikes into 2 to represent one for each fighter
    def strikes_per_body_part(x,y):
        x[y] = x[y].str.replace(' of ', 'of', regex=False)
        x[[y+' F_1', y+' F_2']] = x[y].str.split('  ', expand=True)
        x[[y+' landed F_1', y+' thrown F_1']] = x[y+' F_1'].str.split('of', expand=True)
        x[y+' landed F_1'] = x[y+' landed F_1'].apply(pd.to_numeric, errors='coerce')
        x[y+' thrown F_1'] = x[y+' thrown F_1'].apply(pd.to_numeric, errors='coerce')
        x[[y+' landed F_2', y+' thrown F_2']] = x[y+' F_2'].str.split('of', expand=True)
        x[y+' landed F_2'] = x[y+' landed F_2'].apply(pd.to_numeric, errors='coerce')
        x[y+' thrown F_2'] = x[y+' thrown F_2'].apply(pd.to_numeric, errors='coerce')
    
        return x[y+' landed F_1'],x[y+' thrown F_1'],x[y+' landed F_2'],x[y+' thrown F_2']
    
    # Get Head strikes
    strikes_head = strikes_per_body_part(fight_details_df.copy(), 'Head')
    fight_details_df['Head landed F_1'] = strikes_head[0]
    fight_details_df['Head thrown F_1'] = strikes_head[1]
    fight_details_df['Head landed F_2'] = strikes_head[2]
    fight_details_df['Head thrown F_2'] = strikes_head[3]
    
    # Get Body strikes
    strikes_body = strikes_per_body_part(fight_details_df.copy(), 'Body')
    fight_details_df['Body landed F_1'] = strikes_body[0]
    fight_details_df['Body thrown F_1'] = strikes_body[1]
    fight_details_df['Body landed F_2'] = strikes_body[2]
    fight_details_df['Body thrown F_2'] = strikes_body[3]
    
    # Get Leg strikes
    strikes_leg = strikes_per_body_part(fight_details_df.copy(), 'Leg')
    fight_details_df['Leg landed F_1'] = strikes_leg[0]
    fight_details_df['Leg thrown F_1'] = strikes_leg[1]
    fight_details_df['Leg landed F_2'] = strikes_leg[2]
    fight_details_df['Leg thrown F_2'] = strikes_leg[3]
    
    # Get Distance strikes
    strikes_Distance = strikes_per_body_part(fight_details_df.copy(), 'Distance')
    fight_details_df['Distance landed F_1'] = strikes_Distance[0]
    fight_details_df['Distance thrown F_1'] = strikes_Distance[1]
    fight_details_df['Distance landed F_2'] = strikes_Distance[2]
    fight_details_df['Distance thrown F_2'] = strikes_Distance[3]
    
    # Get Clinch strikes
    strikes_Clinch = strikes_per_body_part(fight_details_df.copy(), 'Clinch')
    fight_details_df['Clinch landed F_1'] = strikes_Clinch[0]
    fight_details_df['Clinch thrown F_1'] = strikes_Clinch[1]
    fight_details_df['Clinch landed F_2'] = strikes_Clinch[2]
    fight_details_df['Clinch thrown F_2'] = strikes_Clinch[3]
    
    # Get Ground strikes
    strikes_Ground = strikes_per_body_part(fight_details_df.copy(), 'Ground')
    fight_details_df['Ground landed F_1'] = strikes_Ground[0]
    fight_details_df['Ground thrown F_1'] = strikes_Ground[1]
    fight_details_df['Ground landed F_2'] = strikes_Ground[2]
    fight_details_df['Ground thrown F_2'] = strikes_Ground[3]
        
        
    #-------------------------------------------------------------------------------------------------
    
    # Create dataframe of fighter names 
    def get_names():
        file2 = ('../data/fighters.csv')
        fighters_ = pd.read_csv(file2)
        fighters_.fillna('', inplace=True)
        fighter_name_ = list(fighters_['First Name'] + ' '+ fighters_['Last Name'])
        fighter_name_ =[x.strip(' ') for x in fighter_name_]
        fighter_name = pd.DataFrame({'Names':fighter_name_})
        return fighter_name
    
   # Get the fighter names
    names = get_names()
    
   #-------------------------------------------------------------------------------------------------
   
   # Using the names dataframe created, split out the fighters names from the Fighter Column
    def fighter_names(frame):
         frame['Fighter 1'] = ''
    
         for x in range(len(names)):
            frame['Fighter 1'] = np.where(frame['Fighter'].str.startswith(names.loc[x,'Names']), 
                                          names.loc[x,'Names'], 
                                          frame['Fighter 1'])
        
         frame['F1 name len'] = frame['Fighter 1'].str.len()
         frame['name len'] = frame['Fighter'].str.len()
         frame['F2 name len'] = frame['name len'] - frame['Fighter 1'].str.len()
         frame['Fighter 2'] = ''
        
         for x in range(len(frame)):
             y = frame.iloc[x]['F2 name len']
            
             frame.loc[x,'Fighter 2'] = frame.iloc[x]['Fighter'][-y:]
            
         frame['Fighter 2'] = frame['Fighter 2'].str.strip()

         return frame['Fighter 1'],frame['Fighter 2']
    
    # Get the names of each fighter in the fight
    fighters = fighter_names(fight_details_df.copy())
    fight_details_df['Fighter 1'] = fighters[0]
    fight_details_df['Fighter 2'] = fighters[1]
        
    #-------------------------------------------------------------------------------------------------
    
    # Reorder columns and remove uneeded columns
    def clean_dataframe(frame):
        frame = frame.reindex(columns=['Event','Fighter 1','KD F_1','Sig. str. landed F_1', 
                                        'Sig. str. thrown F_1','Sig. str. % F_1','Total str. landed F_1', 
                                        'Total str. thrown F_1', 'Td completed F_1','Td attempted F_1',
                                        'Td % F_1','Sub. att F_1','Rev. F_1','Ctrl F_1', 'Head landed F_1', 
                                        'Head thrown F_1','Body landed F_1','Body thrown F_1','Leg landed F_1', 
                                        'Leg thrown F_1','Distance landed F_1','Distance thrown F_1','Clinch landed F_1', 
                                        'Clinch thrown F_1','Ground landed F_1', 'Ground thrown F_1','Fighter 2',
                                        'KD F_2', 'Sig. str. landed F_2','Sig. str. thrown F_2', 
                                        'Sig. str. % F_2','Total str. landed F_2','Total str. thrown F_2', 
                                        'Td completed F_2','Td attempted F_2', 'Td % F_2','Sub. att F_2', 
                                        'Rev. F_2','Ctrl F_2', 'Head landed F_2', 'Head thrown F_2',
                                        'Body landed F_2','Body thrown F_2','Leg landed F_2','Leg thrown F_2', 
                                        'Distance landed F_2','Distance thrown F_2','Clinch landed F_2',
                                        'Clinch thrown F_2','Ground landed F_2','Ground thrown F_2' 
                                        ])
        
        return frame
      
    # Final column cleaning and export completed dataframe
    frame = clean_dataframe(fight_details_df)    
    fight_details_df = frame
    
    return fight_details_df

#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


# Get the fight information, print column info and export CSV
fight_details_df = get_fights()
fight_details_df.info()
fight_details_df.dtypes
#fight_details_df.to_csv('../data/fights.csv')

# =============================================================================
# file =('../data/fights.csv')
# fight_details_df = pd.read_csv(file)
# 
# 
# =============================================================================


