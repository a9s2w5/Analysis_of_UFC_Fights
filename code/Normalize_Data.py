# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:32:54 2021

@author: Jonathan Flanagan (x18143890)
"""
# imports
import pandas as pd
import numpy as np
import Scraper as scrp

#----------------------------------------------------------------------------------------

"""
    Get the Figther, Fighter Additional Details, Event Details, 
    Event Fight Details as DataFrames for our 4 Datasets
    
    Main Dataset is the details from each event 
    and complimentary data sets are the fighter, 
    fighter details and fight details datasets.
    
    In total 10,658 unique url's are scraped in the process and can take several 
    hours to complete depending on computer hardware and internet bandwidth. 
    
    For my personal computer hardware / internet bandwidth combination it took:
    42min 57sec to scrape and retrieve all datasets.
"""

# Get the Fighter Basic Information
print("\nGetting Fighters .....\n")
fighters_df = scrp.get_fighters()

# Get additional Fighter details
print("\nGetting Fighter Details....\n")
fighter_details_df = scrp.get_further_fighter_details()

# Get the events and their details
print("\nGetting Event Details.....\n")
event_details_df = scrp.get_event_details()


# Get the details of each fight at each event
print("\nGetting Fight Details.....\n")
fight_details_df = scrp.get_event_fight_details()

#----------------------------------------------------------------------------------------


