#Quest: Shark Attacts

## \*\*Business proposition

Due to Florida's tourism, Governor Ronald Dion DeSantis has contacted Vaughn Analysts Inc. to analyze shark attacts around Florida.

## \*\*Data to be analyzed

As part of the data exploration, Vaughn Analysts Inc. found a Global Shark Attack File. (https://www.sharkattackfile.net/incidentlog.htm). The data for analysis was retreaved from this site, espefifically from this link: https://www.sharkattackfile.net/spreadsheets/GSAF5.xls

### Hypothesis

#### Univariate analysis

1. Shark attacts are more common among individuals swimming.
2. Shark attacts are more common during the afternoon.
3. Shark attacts are more common if the sharks are provoked.
4. Shark attacts are more common to males.
5. Shark attacts are more common during the summer months.
6. Shark attacts are more common among people under 30 years old.

## \*\*Data cleaning

### Downloading the file and additional libraries

The first step into the data cleaning is to download the file into Python. In this case, a Jupyter Notebook is going to be used.
Pandas library needs to be imported before creating the dataframe.
'''python
import numpy as np
import pandas as pd
url = "https://www.sharkattackfile.net/spreadsheets/GSAF5.xls"
shark_data = pd.read_excel(url)
'''

### Taking a look at the data

To identify were the data needs cleaning, the data must be looked at. With the following code one can see the columns and how the data is presented in the table.
'''python
shark_data.head(5)
'''
To get a better picture of how big the data is, the following code will be used to determine number if rows and columns respectively.
'''python
initial_data_shape=shark_data.shape
initial_data_shape
'''
Python returns (6969, 23). Meaning 6969 rows and 23 columns.
Each column has a name. The name for the columns can be identified with:
'''python
shark_data.columns
'''

### Cleaning the data per columns

First, considering the Country column the ones that are not USA will be eliminated from the dataframe.
To do that the following code will show if the USA is written in different ways.
'''python
shark_data.Country.unique()
'''
Given that there is only one way USA was written, the next step is to create that new dataframe without the other Counties.
'''python
usa_data = shark_data[shark_data['Country'] == 'USA']
'''
To select only data from Florida, the same procedure will be followed for the State column.
'''python
shark_data.State.unique()
'''
To select the 3 different ways Florida is written, the following code was used:
'''python
florida_data = usa_data[usa_data['State'].isin(['Florida', 'Franklin County, Florida'])]
'''
To continue the cleaning, various columns that added no value into answering the hypothesis where removed. Only leaving 'Date', 'Type', 'Activity', 'Sex', 'Age', 'Time' and 'Species '.
'''python
useful_columns = ['Date', 'Type', 'Activity', 'Sex', 'Age', 'Time', 'Species ']
filtered_data = florida_data[useful_columns]
filtered_data.columns
'''

### Cleaning the data per rows

First, the data es check for duplicates.
'''python
filtered_data.duplicated().sum()
'''
Now the Type colummn's names are verified.
'''python
filtered_data['Type'].unique()
'''
All the null values in Type will be deleted.
'''python
filtered_data_cleaned = filtered_data.dropna(subset=['Type'])
'''
Fixing the misspell on Provoked.
'''python
filtered_data_cleaned['Type'] = filtered_data_cleaned['Type'].str.strip().replace(' Provoked', 'Provoked')
'''
Type can be transformed to 'Provoked', 'Unprovoked' and 'Questionable'.
'''python
filtered_data_cleaned['Type'] = filtered_data_cleaned['Type'].apply(lambda x: 'Questionable' if x not in ['Provoked', 'Unprovoked'] else x)
'''
To count the amount of incidents per Type of incident.
'''python
filtered_data_cleaned['Type'].value_counts()
'''

#### Hypothesis #3

With his information, the hypothesis #3 gets rejected. Shark attacts are not more common if the sharks are provoked.

Now the Activity colummn's names are verified.
'''python
filtered_data_cleaned['Activity'].unique()
'''
To clean the Activity column a library must be downloaded.
'''python
import re
'''
Then the following code will be used to identify code word on the string.
'''python
pattern_1 = re.compile(r'._fishing._', flags=re.IGNORECASE)
pattern_2 = re.compile(r'._swimming._', flags=re.IGNORECASE)
pattern_3 = re.compile(r'._surfing._', flags=re.IGNORECASE)
pattern_4 = re.compile(r'._wading._', flags=re.IGNORECASE)
'''
After the patter of recognition has been created, the data will be changed to match that pattern.
'''python
def activity_def(df,activity,pattern, action ):
return df.loc[df[activity].str.contains(pattern, na=False), activity] == action
activity_def(filtered_data_cleaned,'Activity',pattern_1,'Fishing')
activity_def(filtered_data_cleaned,'Activity',pattern_2,'Swimming')
activity_def(filtered_data_cleaned,'Activity',pattern_3,'Surfing')
activity_def(filtered_data_cleaned,'Activity',pattern_4,'Walking')
'''
The null values were changed to Unknown.
'''python
filtered_data_cleaned['Activity'].fillna('Unknown', inplace=True)
'''
With the funtion .value_counts, the types of activities can be counted.
'''python
filtered_data_cleaned['Activity'].value_counts().head(3)
'''

#### Hypothesis #1

With that last code, the hypothesis gets rejected. Shark attacts are not more common among individuals swimming.

The Sex column's information gets looked at to verify for differences in inputs.
'''python
filtered_data_cleaned['Sex'].unique()
'''
The Sex column's null values get changed to Unkown.
'''python
filtered_data_cleaned['Sex'].fillna('Unknown', inplace=True)
'''
Some of the Sex data needs transformatio. The next code helps eliminate the spaces before and after the words.
'''python
filtered_data_cleaned['Sex'] = filtered_data_cleaned['Sex'].str.strip()
'''
The value counts can be used to prove the hypothesis #5.
'''pyhon
filtered_data_cleaned['Sex'].value_counts()
'''

#### Hypothesis #4

The hypotheis shark attacts are more common in males, gets accepted.

When looking at the Date column:
'''python
filtered_data_cleaned['Date'].unique()
'''
The date column gives too much information not needed in the analysis. Only the month is going to be used for the analysis.
For that the column's null values with Unknown.
'''python
filtered_data_cleaned['Date'].fillna('Unknown', inplace=True)
'''
First, Python need to know the patter that has to recognice in the string. For that:
'''python
pattern = re.compile(r'(?i)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)')
'''
Then, a new column Month is created. This column will only hold the month information based on the pattern recognition created before.
'''python
filtered_data_cleaned['Month'] = filtered_data_cleaned['Date'].str.extract(pattern, expand=False)
'''
The shark attacts per month can be seen in this code:
'''python
month_counts = filtered_data_cleaned['Month'].value_counts()
month_counts
'''

#### Hypothesis #5

The hypotheis: shark attacts are more common during the summer months; is rejected. September was the month with more chark attacts.

Since, a new column for month was created, the column for Date can be eliminated.
'''python
filtered_data_cleaned.drop(columns=['Date'], inplace=True)
'''
Regarding the Age column, the following code can be used to see the different inputs:
'''python
filtered_data_cleaned['Age'].unique()
'''
All values should be strings.
'''pyhton
filtered_data_cleaned['Age'] = filtered_data_cleaned['Age'].astype(str)
'''
The spaces should be removed.
'''pyhton
filtered_data_cleaned['Age'] = filtered_data_cleaned['Age'].str.strip()
pattern = re.compile(r'(\d{1,2})')
'''
The data after the cleaning should only have the first two chracters as defined in the pattern.
'''python
filtered_data_cleaned['Age'] = filtered_data_cleaned['Age'].apply(lambda x: pattern.match(x).group(1) if pattern.match(x) else np.nan)
'''
Now the null values will be filled with the foward value.
'''python
filtered_data_cleaned['Age'].fillna(method='ffill', inplace=True)
'''
Now the data type will be changed to integer.
'''python
filtered_data_cleaned['Age'] = filtered_data_cleaned['Age'].astype(float).astype('Int64')
'''
the count of the total shark attacts per sex can be found with:
'''python
filtered_data_cleaned['Age'].value_counts()
'''

#### Hypothesis #6

The hypothesis is acepted. Shark attacts are more common among people under 30 years old.
This grapth includes a more visual way of displaying the data.
'''python
import seaborn as sns
sns.histplot(filtered_data_cleaned['Age'], bins=100)
'''
Moving to the Time column, the unique inputs are verified
'''python
filtered_data_cleaned['Time'].unique()
'''
Then the format is verified with:
'''python
filtered_data_cleaned['Time'].dtype
'''
Then this function is created to categorize the time:
'''python
def categorize_time(time):
if pd.isna(time): # Check if the value is NaN
return np.nan

    # Convert to string
    time_str = str(time)

    # Extract hour from the time string
    if 'h' in time_str:
        hour = time_str.split('h')[0]  # Extract hour if 'h' separator is present
        if hour.isdigit():
            hour = int(hour)
        else:
            return np.nan  # Return NaN if hour is not a valid integer
    elif ':' in time_str:
        hour = time_str.split(':')[0]  # Extract hour if ':' separator is present
        if hour.isdigit():
            hour = int(hour)
        else:
            return np.nan  # Return NaN if hour is not a valid integer
    else:
        return np.nan  # Return NaN if neither separator is found

    # Categorize the time into MORNING, AFTERNOON, or EVENING
    if hour < 12:
        return 'MORNING'
    elif hour < 18:
        return 'AFTERNOON'
    else:
        return 'EVENING'

'''
That function is applied to clean the column Time with this code:
'''python
filtered_data_cleaned['Time'] = filtered_data_cleaned['Time'].apply(categorize_time)
'''
Then the total null values in Time is calculated.
'''python
total_nulls = filtered_data_cleaned['Time'].isnull().sum()
'''
Then a ratio tu fill the null values is created based on
'''python
afternoon_nulls = round((53/99) _ total_nulls)
morning_nulls = round((32/99) _ total_nulls)
evening_nulls = round((10/99) \* total_nulls)
'''
Then those ratios are used to fill in the nulls with the 3 possible inputs afternoon, morning and evening.
'''python
filtered_data_cleaned['Time'].fillna('AFTERNOON', limit=afternoon_nulls, inplace=True)
filtered_data_cleaned['Time'].fillna('MORNING', limit=morning_nulls, inplace=True)
filtered_data_cleaned['Time'].fillna('EVENING', limit=evening_nulls, inplace=True)
'''
To verify the input with highest frecuency in the Time category, the next code was used:
'''python
filtered_data_cleaned['Time'].value_counts()
'''
This code helps visualize the category Time.
'''python
sns.histplot(filtered_data_cleaned['Time'], bins=100)
'''

#### Hypothesis #2

The time of day with most shark attacts is the afternoon. The hypothesis gets accepted.
