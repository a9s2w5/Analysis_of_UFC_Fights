# An Analysis of UFC Fights
An analysis of Mixed Martial Arts fights taken place under the promotion of the Ultimate Fighting Championship (UFC).

# Data Collection
Data for this analysis has been collected through http://www.ufcstats.com <br>
<br>
In total 10,658 unique url's where processed, Using this program to collect the data <br>
can take several hours to complete depending on computer hardware and internet bandwidth.<br>
    
For my personal computer hardware / internet bandwidth combination it took:<br>
**_Approx 4hrs_** to retrieve all data.<br>
<br>
To collect the Data, Normalize_Data.py can be ran which will update the data contained in the csv files.<br>
Data is updated on the website after each new fight event.<br>
**Running the Normalize_Data.py script will initiate these methods:**<br>

#### 1. Getting the fighter info & normalizing
```python
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
    
    # More code below here for normalization......
    
    return fighters_df
    
# Get the figthers information and export to CSV
fighters_df = get_fighters()
fighters_df.to_csv('../data/fighters.csv', index=False)
```


# Data Info
There are 3 Datasets contained in the Data folder. <br>
- Fighter Information (fighters.csv)
- Events Information (events.csv)
- Fights Information (fight_data.csv)

### The Fighter information
This is the data information in the fighters.csv file <br>
*_(After normalization and export but before cleaning and dealing with null/missing values)_*<br><br>
![Fighter Data Info](https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/fighter_dtypes_info.png)
<br>
<br>
Fighter Table Info snippet: <br><br>
![Fighter Table Snippet](https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/fighter_info_head.png)

# Tools Used
All tools and languages used, including packages from within each language <br>
<br>
#### Prerequisites are:
- Python3 is instaled
- R and R Studio are installed
- Anaconda3 is installed

##### Installing Anaconda Instructions: <br>
**For Windows:** https://docs.anaconda.com/anaconda/install/windows/ <br>
**For Mac**: https://docs.anaconda.com/anaconda/install/mac-os/ <br>
**For Linux:** https://docs.anaconda.com/anaconda/install/linux/ <br>

##### Installing R & R Studio: <br>
Instructions here: https://rstudio-education.github.io/hopr/starting.html <br>

## Python 
Spyder IDE from within the Anaconda3 framework
#### Packages Imported:
- Pandas<br>
- Numpy <br>
- string<br>
- tqdm<br>
- BeautifulSoup<br>
- requests<br>

## R
R Studio

