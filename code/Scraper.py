# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:32:54 2021

@author: Jonathan Flanagan (x18143890)
"""

"""
    This module is for extracting the neccessary Data from http://www.ufcstats.com
    a website that keeps all data for mixed martial artists as well as fights completed
    under the UFC Mixed Martial Arts promotion.
    
    This module only scrapes the data and does not perform cleaning or first normal form
    operations on the data. It is meant to be imported into Normalize_Data.py and ran where
    4 Datasets are retrieved ready for first normal form opertations and data preperation/cleaning.
"""

# imports
import pandas as pd
import string
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests

#----------------------------------------------------------------------------------------

"""
    This class is used for some of the scraping material that can be generalised and 
    abstraced out to avoid redundancy. 
    
    There are some methods in this module that could possibly use methods from within 
    this Class but as they need different attributes to be appended during the scrape 
    to keep data susinct, I have left them as their own complete methods. 
    
"""
# Class to scrape different items from a single webpage or list of webpages 
class Scraper:
     
    # Scrape for table / tables using pandas
    def pd_scrape_tables(self,urlList):
        
        dfl=[]
        df = pd.DataFrame()
        
        if len(urlList) > 1:
            try:
               # Scrape the URLs and create DataFrames for first table on each page
               for url in tqdm(range(len(urlList)), desc="Scraping URL's: "):
                   data = pd.read_html(urlList[url])
                   dfl.append(data[0]) 
              
               # Concatenate all collected DataFrames
               for i in tqdm(range(len(dfl)), desc="Creating DataFrame: "):
                    df = df.append(dfl[i])   
               return df
            except ValueError:
                 print("\nNo tables found!")
        elif len(urlList) == 1:
            try:
                # Scrape the single URL and get the first table on the page
                data = pd.read_html(urlList[0])
                # append dataframe to list
                dfl.append(data[0])
                # append list item to main dataframe
                df = df.append(dfl[0]) 
                return df
            except ValueError:
                print("\nNo Table found!")
        else:
            print("\nList has no objects!")
    
    
    # scrape for links from a page(s) by tag and class using Beautiful Soup
    def scrape_links(self, urlList, tag, className):
        
        links = []
        
        # Scrape for links
        if len(urlList) > 1:
            try:
              for url in tqdm(range(len(urlList)), desc="Scraping URL's: "):
                    # Get the url and convert with html.parser
                    page = requests.get(urlList[url])
                    soup = BeautifulSoup(page.text, 'html.parser')
                    soup
            
                    
                    # Get the tag for the class present on the webpage
                    x = soup.find(tag, {'class': className})
                    # Get the links present on the page
                    links__ = [a.get('href') for a in x.find_all('a', href=True)]
                    # remove duplicates by creating a dict
                    links_ = list(dict.fromkeys(links__))
                    # add to the original blank list
                    links.extend(links_)
                    
              return links
            except ValueError:
                print("\n Nothing to do!")
        elif len(urlList) == 1:
            try:
                 # Get the url and convert to lxml
                 page = requests.get(urlList[0])
                 soup = BeautifulSoup(page.text, 'lxml')
                 soup
               
                 # Get the tag for the class present on the webpage
                 x = soup.find(tag, {'class': className})
                 # Get the links present on the page
                 links__ = [a.get('href') for a in x.find_all('a', href=True)]
                 # remove duplicates by creating a dict
                 links__ = list(dict.fromkeys(links__))
                 # add to the original blank list
                 links.extend(links__)
                 
                 return links
            except ValueError:
                print("\nNothing to do!")
        else:
            print("No pages to scrape")
            
#----------------------------------------------------------------------------------------

# create the list of urls for all the basic fighter details pages
def fighter_url_list():
    # Target url for fighters
    url_fighters = "http://ufcstats.com/statistics/fighters"
    
    fighter_urls=[]
    
    # alphabetical search
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    
    # Gather all the URLs to be scraped
    for letter in tqdm(alphabet_list, desc="Creating URL's"):
        criteria = "?char=" + letter + "&page=all"
        url_complete = url_fighters + criteria 
        fighter_urls.append(url_complete)
    
    return fighter_urls

#----------------------------------------------------------------------------------------

# Create DataFrame from the URL list
def get_fighters():
    # Instantiate PandasScraper           
    f = Scraper()
    
    # scrape for the fighters
    fighters_df = f.pd_scrape_tables(fighter_url_list())
    
    # Seen as the first row for each table is empty, drop it
    fighters_df = fighters_df.dropna(axis=0, how='all')
    # Reset the Index
    fighters_df.reset_index(drop=True, inplace=True)
    
    return fighters_df

#----------------------------------------------------------------------------------------

# Create DataFrame for the Fight Events
def get_event_names():
    # Instantiate PandasScraper           
    e = Scraper()
    
    # scrape for the events
    eventUrls = ["http://ufcstats.com/statistics/events/completed?page=all"]
    events_df = e.pd_scrape_tables(eventUrls)
    
    # we know from the webpage that the first and second rows are not needed
    # first row is blank & second row is for the next upcoming fight
    events_df.drop(index = 0,inplace = True)
    events_df.drop(index = 1, inplace= True)
    
    # reset the index
    events_df.reset_index(drop = True, inplace=True)
    
    return events_df

#----------------------------------------------------------------------------------------

# create a list of urls for all the event details from the events page
def get_event_detail_URLs():
    # Instantiate the Scraper
    l = Scraper()
    
    # the events page url
    url = ["http://ufcstats.com/statistics/events/completed?page=all"]
    # the tag to vbe looked for
    tag= 'table'
    # the tag class to be looked for
    className = 'b-statistics__table-events'
    
    # Get the event URL's
    event_detail_URLs = l.scrape_links(url, tag, className)
    
    # remove the first url as it is for an upcomimg fight
    event_detail_URLs.pop(0)
    
    return event_detail_URLs

#----------------------------------------------------------------------------------------

"""
    This function we don't invoke the Scraper Class as we need to append to the rows from 
    a list as we create the DataFrames.
"""

def get_event_details():
    event_details_dfs = []
    event_details_df = pd.DataFrame()
    
    # Get the event details URL's and the event names
    event_detail_URLs = get_event_detail_URLs()
    event_names_df = get_event_names()
    
    # Scrape the URLs and create DataFrames for each table adding the event name from df_events
    for url in tqdm(range(len(event_detail_URLs)), desc="Scraping URL's: "):
        data = pd.read_html(event_detail_URLs[url])
        data[0]['Event'] = event_names_df['Name/date'][url]
        event_details_dfs.append(data)
    
     # Concatenate all collected DataFrames
    for i in tqdm(range(len(event_details_dfs)), desc="Creating DataFrame: "):
        event_details_df = event_details_df.append(event_details_dfs[i])
    
    # Reset the index
    event_details_df.reset_index(drop=True, inplace=True)
    
    return event_details_df

#----------------------------------------------------------------------------------------

# Get the URL's for further fighter details
def get_fighter_more_details_URLs():
    # Instantiate the Scraper
    fd = Scraper()
    
    # URL List
    urls = fighter_url_list() 
    
    # the tag to be looked for
    tag= 'table'
    # the tag class to be looked for
    className = 'b-statistics__table'
    
    # Get the URL list for more fighter info
    fighter_more_details_URLs = fd.scrape_links(urls, tag, className)
    
    
    return fighter_more_details_URLs

#----------------------------------------------------------------------------------------

"""
    This function we don't invoke the Scraper Class as we need to append two items together
    during the scrape.
"""

# Get the additional Fighter details from the the created URL list
def get_further_fighter_details():
    
    fighter_details_df = pd.DataFrame(columns=('Name','Height','Weight','Reach','Stance','DOB'))
    
    fighter_details_urls = get_fighter_more_details_URLs()
    
    for url in tqdm(range(len(fighter_details_urls)), desc='Getting Fighter Details: '):
        # Get the url and convert to lxml
        page = requests.get(fighter_details_urls[url])
        soup = BeautifulSoup(page.text, 'lxml')
        soup
    
        # Get the title name present on the webpage
        name__ = soup.find('span', {'class': 'b-content__title-highlight'})
        name = name__.text.strip()
        # Get the details list items
        details__ = soup.find('ul', {'class': 'b-list__box-list'})
        details = [a.text.replace('\n','').replace('--', '').replace(' ','') for a in details__.find_all('li')]
        # append the name to the begining of the details list
        details.insert(0, name)
        # append each list as a row to the DataFrame
        fighter_details_df.loc[len(fighter_details_df)] = details
    
    return fighter_details_df      

#----------------------------------------------------------------------------------------

# Get the URL's for event fight details
def get_event_fight_detail_URLs():
    # Instantiate the Scraper
    efd = Scraper()
    
    # event URLs 
    event_urls = get_event_detail_URLs()
    
    # the tag to be looked for
    tag= 'table'
    # the tag class to be looked for
    className = 'b-fight-details__table'
    
    # Get the URL list for the fight details
    fight_detail_URLs = efd.scrape_links(event_urls, tag, className)
    
    # Only keep URLs referencing a fights details
    fight_detail_URLs[:] = [x for x in fight_detail_URLs if "http://ufcstats.com/fight-details" in x]
    
    return fight_detail_URLs


#----------------------------------------------------------------------------------------

"""
    This function we don't invoke the Scraper Class as we need to append two items together
    during the scrape aand use different attributes from different tables on each page
"""

# Get the fight details from each event
def get_event_fight_details():
    
    # Fight detail URLs
    fight_detail_URLs = get_event_fight_detail_URLs()

    # List of scapred DataFrames
    fight_details_dfs = []
    
    # Main DataFrame
    fight_details_df = pd.DataFrame()
    
    # Scrape for the fight details from each URL
    for url in tqdm(range(len(fight_detail_URLs)), desc="Getting Fight Details: "):
        # Get the url and convert to lxml
        page = requests.get(fight_detail_URLs[url])
        soup = BeautifulSoup(page.text, 'lxml')
        soup
    
        # Get the title name present on the webpage
        event__ = soup.find('h2', {'class': 'b-content__title'})
        event = event__.text.strip()
        
        # Get the fight details tables, joining relevant data together
        data = pd.read_html(fight_detail_URLs[url])
        
        # Add the details from the third table to the first table
        data[0][['Head',
                'Body',
                'Leg',
                'Distance',
                'Clinch',
                'Ground']] = data[2][['Head',
                                      'Body',
                                      'Leg',
                                      'Distance',
                                      'Clinch',
                                      'Ground']]
        
        # Add the event name to the dataframe
        data[0]['Event'] = event
        # append to list of dataframes
        fight_details_dfs.append(data[0])
                                                                                        
        
     # Concatenate all collected DataFrames
    for i in tqdm(range(len(fight_details_dfs)), desc="Creating DataFrame: "):
        fight_details_df = fight_details_df.append(fight_details_dfs[i])
        
    
    # Reset the index
    fight_details_df.reset_index(drop=True, inplace = True)
        
        
    return fight_details_df

#----------------------------------------------------------------------------------------














