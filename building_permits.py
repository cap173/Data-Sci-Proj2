import requests
import time
import csv
import json
import pandas as pd

url_permits_2010 = 'https://opendata.arcgis.com/datasets/ffd15e5b0d4046c4b904b11360fe66bc_11.csv'
permits2010 = 'permits_2010.csv' 

url_permits_2018 = 'https://opendata.arcgis.com/datasets/42cbd10c2d6848858374facb06135970_9.csv'
permits2018 = 'permits_2018.csv'

def collectData(url, filename):
   request = requests.get( url )
   outFile = open( filename, 'wt' )
   outFile.write( request.text.encode('utf-8'))
   
def file_to_df( filename ):
    myData = pd.read_csv( filename , sep=',', encoding='latin1')
    return myData

def df_to_file(df, filename):
    file_from_df = df.to_csv(filename, index=False, encoding='latin1')
    return file_from_df


def clean_data(filename):
    # Opens the csv with data so it can be cleaned 
    data = file_to_df( filename )
    # Remove rows with missing data and print them onto screen 
    # Display how many rows were dropped
    labels = ['PERMIT_CATEGORY_NAME','CITY', 'STATE', 'ZIPCODE', 'DCSTATADDRESSKEY', 'DCSTATLOCATIONKEY','HOTSPOT2006NAME', 'HOTSPOT2005NAME', 'HOTSPOT2004NAME', 'BUSINESSIMPROVEMENTDISTRICT']
    data = data.drop(labels, axis=1)
    # remove 7 PM time from column
    data['ISSUE_DATE'] = data['ISSUE_DATE'].str[:10]
    if('2018' in filename):
        data['LASTMODIFIEDDATE'] = data['LASTMODIFIEDDATE'].str[:10]
        

    df_filename = filename[:-4] + "_CLEAN.csv"
    df_to_file(data, df_filename)
    return data
    
def main():
    collectData(url_permits_2010, permits2010)
    df_permits2010 = clean_data(permits2010)
    # sometimes pulling this data throws an error...
    # I guess it's sending too many requests at a time
    time.sleep(30)
    collectData(url_permits_2018, permits2018)
    df_permits2018 = clean_data(permits2018)

if __name__== "__main__" :
    main()