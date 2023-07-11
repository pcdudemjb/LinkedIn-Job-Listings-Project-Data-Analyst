import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

canada = pd.read_csv('linkedin-jobs-canada.csv')
usa = pd.read_csv('linkedin-jobs-usa.csv')

canada.info()
# RangeIndex: 2773 entries, 0 to 2772
# Data columns (total 9 columns):
#   Column         Non-Null Count  Dtype 
#---  ------         --------------  -----
# 0   title          2773 non-null   object
# 1   company        2773 non-null   object
# 2   description    2773 non-null   object
# 3   onsite_remote  2773 non-null   object
# 4   salary         36 non-null     object
# 5   location       2773 non-null   object
# 6   criteria       2773 non-null   object
# 7   posted_date    2773 non-null   object
# 8   link           2773 non-null   object
# dtypes: object(9)

usa.info()
# RangeIndex: 2845 entries, 0 to 2844
#Data columns (total 9 columns):
#   Column         Non-Null Count  Dtype
#---  ------         --------------  -----
# 0   title          2845 non-null   object
# 1   company        2845 non-null   object
# 2   description    2845 non-null   object
# 3   onsite_remote  2845 non-null   object
# 4   salary         929 non-null    object
# 5   location       2845 non-null   object
# 6   criteria       2845 non-null   object
# 7   posted_date    2845 non-null   object
# 8   link           2845 non-null   object
# dtypes: object(9)

# Expecting 5618 rows after concatenation
n_america = pd.concat([canada, usa])

n_america.info()
# Int64Index: 5618 entries, 0 to 2844
#Data columns (total 9 columns):
#   Column         Non-Null Count  Dtype
#---  ------         --------------  -----
# 0   title          5618 non-null   object
# 1   company        5618 non-null   object
# 2   description    5618 non-null   object
# 3   onsite_remote  5618 non-null   object
# 4   salary         965 non-null    object
# 5   location       5618 non-null   object
# 6   criteria       5618 non-null   object
# 7   posted_date    5618 non-null   object
# 8   link           5618 non-null   object
# dtypes: object(9)

n_america.to_csv('n_america.csv', index=False)

#------------------------------------------------------------------------------#
####  Thoughts/Ideas ####

# Interested in seeing repeats in companies hiring

# Descriptions... (Omitting for now.  May perform some NLP in the future.)

# Curious about the percentage of remote opportunities

# Data only contains 17% of information regarding salary...

# Locations might be interesting to plot with Tableau

# Criteria...  (Omitting for now.  May perform some NLP in the future.)

# Posted date may show trends of job opportunities

# Links probably won't be beneficial
#------------------------------------------------------------------------------#

# 1.  Checking for companies hiring multiple positions/multiple job postings
companies = n_america["company"].value_counts().head(10)
print(companies)
# PayPal              499
# SSENSE              133
# Synechron           110
# Insight Global      106
# Diverse Lynx        101
# Citi                 76
# theScore             72
# Circle K             72
# Onlia                72
# Agility Partners     69

#------------------------------------------------------------------------------#

# 2.  Descriptions  (Omitting for now.  May perform some NLP in the future.)

#------------------------------------------------------------------------------#

# 3.  How many of these postings are remote
n_america['onsite_remote'].value_counts()
# onsite    1925
# hybrid    1875
# remote    1818

# 32.4% Fully remote positions

#------------------------------------------------------------------------------#

# 4.  Let's compare salary information
# (Some job positings are hourly and some are annually)

# Split the numbers from the range
n_america['salary'].value_counts()

def extract_first_number(salary):
    if isinstance(salary, str):
        salary_parts = salary.split('-')
        first_number = salary_parts[0].strip()
        return first_number
    else:
        return None

n_america['salary_low'] = n_america['salary'].apply(extract_first_number)

n_america.info()

def extract_second_number(salary):
    if isinstance(salary, str):
        salary_parts = salary.split('-')
        second_number = salary_parts[1].strip()
        return second_number
    else:
        return None

n_america['salary_high'] = n_america['salary'].apply(extract_second_number)

n_america.info()

# Recode to new df
n_americaR = n_america
n_americaR.info()

# Drop NA values
n_americaR.dropna(inplace=True)
n_americaR.info()


# Change column types
# There was one Canadian dollar value that needed changing
n_americaR['salary_low'] = n_americaR['salary_low'].str.replace('CA\$|[\$,]', '', regex=True).astype(float)
n_americaR['salary_high'] = n_americaR['salary_high'].str.replace('CA\$|[\$,]', '', regex=True).astype(float)


# Now to change the hourly to salary
n_americaR['salary_lowR'] = ''
n_americaR['salary_highR'] = ''

n_americaR['salary_low'].value_counts(sort=True)
# Highest hourly wage found was $68/hr (salary_low)
n_americaR['salary_high'].value_counts(sort=True)
# Highest hourly wage found was $100/hr (salary_high)
# Canadian values were $135 and $145 (will convert them to USD)
# Some Samsung jobs listed their salaries as monthly.

def convert_hourly_to_yearly(hourly_rate):
    if isinstance(hourly_rate, str):
        hourly_rate = float(hourly_rate)
    if isinstance(hourly_rate, float) and hourly_rate <= 100.00:
        return hourly_rate * 2080  # (40 hours per week * 52 weeks)
    if isinstance(hourly_rate, float) and 135.00 <= hourly_rate <= 145.00:
        return hourly_rate * 2080 * 0.747  # (1 CAD = 0.747 USD)
    if isinstance(hourly_rate, float) and 5800.00 <= hourly_rate <= 6000.00:
        return hourly_rate * 12
    else:
        return hourly_rate

n_americaR['salary_lowR'] = n_americaR['salary_low'].apply(convert_hourly_to_yearly)
    
n_americaR['salary_highR'] = n_americaR['salary_high'].apply(convert_hourly_to_yearly)

salary_range_low = n_americaR['salary_lowR'].describe().astype(int)
print(salary_range_low)
# count       965
# mean      89586
# std       24969
# min       45760
# 25%       70000
# 50%       83200
# 75%      104000
# max      209757

plt.hist(n_americaR['salary_lowR'], bins=10, color='skyblue', edgecolor='black')
# Add labels and title
plt.xlabel('Salary Range')
plt.ylabel('Frequency')
plt.title('Histogram of Salary Range (Low End)')
# Display the histogram
plt.show()


salary_range_high= n_americaR['salary_highR'].describe().astype(int)
print(salary_range_high)
# count       965
# mean     109429
# std       32892
# min       49920
# 25%       90000
# 50%      110000
# 75%      124800
# max      225295

plt.hist(n_americaR['salary_highR'], bins=10, color='skyblue', edgecolor='black')
# Add labels and title
plt.xlabel('Salary Range')
plt.ylabel('Frequency')
plt.title('Histogram of Salary Range (High End)')
# Display the histogram
plt.show()

n_americaR.to_csv('n_americaR.csv', index=False)

#------------------------------------------------------------------------------#

# 5.  Location values from data are not in a coherent format.

import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Initialize geocoder
geolocator = Nominatim(user_agent="my_app")

# Get the city names from the 'location' column in the n_america DataFrame
city_names = n_america['location'].tolist()

# Define batch size for geocoding
batch_size = 100

# Initialize empty lists to store the coordinates
latitudes = []
longitudes = []

# Process the city names in batches
for i in range(0, len(city_names), batch_size):
    # Get a batch of city names
    batch = city_names[i:i+batch_size]
    
    # Geocode each city name in the batch
    for city_name in batch:
        if city_name.lower() in ['united states', 'canada']:
            # Skip geocoding for generic location names
            latitude, longitude = None, None
        else:
            retries = 5  # Number of retries
            while retries > 0:
                try:
                    location = geolocator.geocode(city_name)
                    latitude = location.latitude if location else None
                    longitude = location.longitude if location else None
                    break  # Break out of the retry loop if successful
                except (GeocoderTimedOut, GeocoderUnavailable):
                    # Handle timeout or service unavailable exceptions
                    print(f"Timeout or service unavailable: {city_name}. Retrying...")
                    retries -= 1
                    time.sleep(1)  # Delay before retrying
            
            if retries == 0:
                # Max retries exceeded, assign None values
                print(f"Max retries exceeded for: {city_name}. Skipping...")
                latitude, longitude = None, None
        
        latitudes.append(latitude)
        longitudes.append(longitude)

# Assign the coordinates to new columns in the n_america DataFrame based on the mapped index
n_america['Latitude'] = pd.Series(latitudes, index=n_america.index)
n_america['Longitude'] = pd.Series(longitudes, index=n_america.index)

# Print the updated n_america DataFrame
print(n_america)
n_america['Longitude'].info()
n_america['Latitude'].info()

n_americaMAP = n_america
# n_americaMAP.to_csv('n_americaMAP.csv', index=False) # Commenting out so I don't overwrite the manual additions mentioned below
# Greater Sacramento coordinates show in Australia along with a Charlotte Metro location, now fixed.
# Los Angeles Metro was showing up in Peru, fixed.
# I added some coordinates for location values that were listed as "Metropolitan Area"
# Many Location values simply list Canada & United States.

#------------------------------------------------------------------------------#

# 6.  Looking for trends amongst job types (onsite, hybrid and remote) over time.

# Convert posted_date to datetime
n_america['posted_date'] = pd.to_datetime(n_america['posted_date'])

# Create a new column for the month
n_america['Month'] = n_america['posted_date'].dt.to_period('M')

# Create a dummy column to count occurrences (1 for each row)
n_america['Count'] = 1

# Create a pivot table to count the number of job postings for each type (onsite, hybrid, remote) by month
pivot_table = pd.pivot_table(n_america, values='Count', index='Month', columns='onsite_remote', aggfunc='sum', fill_value=0)

# Plot the pivot table as a grid
fig, ax = plt.subplots(figsize=(10, 6))
pivot_table.plot(kind='bar', stacked=True, ax=ax)

# Customize the plot
plt.title('Job Postings by Type and Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend(title='Job Type')

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()


n_america.sort_values(['posted_date'], inplace=True)
n_america['posted_date'].head()
# Earliest posting is from May 13, 2022

n_america.sort_values(['posted_date'], ascending=False, inplace=True)
n_america['posted_date'].head()
# Latest posting is from Nov 23, 2022

# There aren't many postings from May - Aug in this dataset.

#------------------------------------------------------------------------------#