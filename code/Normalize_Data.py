# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:32:54 2021

@author: Jonathan Flanagan (x18143890)
"""
# imports
import pandas as pd
import Scraper as scrp

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#----------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------

# Get the figthers information and export to CSV
fighters_df = get_fighters()
fighters_df.info()
fighters_df.dtypes
print(fighters_df)
fighters_df.to_csv('../data/fighters.csv', index=False)

#----------------------------------------------------------------------------------------

# Get the events and their details
#print("\nGetting Event Details.....\n")
#event_details_df = scrp.get_event_details()


# Get the details of each fight at each event
#print("\nGetting Fight Details.....\n")
#fight_details_df = scrp.get_event_fight_details()

#----------------------------------------------------------------------------------------














