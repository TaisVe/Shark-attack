# This document includes the functions created for the shark_data. Obtained from "https://www.sharkattackfile.net/spreadsheets/GSAF5.xls".

def activity_def(df,activity,pattern, action ):
  return df.loc[df[activity].str.contains(pattern, na=False), activity] == action
 

def categorize_time(time):
    if pd.isna(time):  # Check if the value is NaN
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