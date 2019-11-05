import requests
import csv
import json
import pandas as pd

url_permits_2010 = 'https://opendata.arcgis.com/datasets/ffd15e5b0d4046c4b904b11360fe66bc_11.csv'
permits2010 = 'permits_2010.csv'
clean_permits2010 = open( 'permits_2011_CLEAN.csv', 'w')

url_permits_2018 = 'https://opendata.arcgis.com/datasets/42cbd10c2d6848858374facb06135970_9.csv'
permits2018 = 'permits_2018.csv'
clean_permits2018 = open( 'permits_2011_CLEAN.csv', 'w')

def collectData():
   # Request 2010 data from API and save it into a csv file
   request = requests.get( url_permits_2010 )
   outFile = open( permits2010, 'wt' )
   outFile.write( request.text.encode('utf-8'))
   
   # Request 2018 data from API and save it into a csv file
   request = requests.get( url_permits_2018 )
   outFile = open( permits2018, 'wt' )
   outFile.write( request.text.encode('utf-8'))
   
   print( outFile )
   
   
def openFile( filename ):
    myData = pd.read_csv( filename , sep=',', encoding='latin1')
    return myData

def removeMissing( data ):
    # Remove rows with missing data and print them onto screen 
    # Display how many rows were dropped
    rowCount = data.shape[0]
    badRows = data[data.isna().any(axis=1)]
    data = data.dropna()
    rowCount = rowCount - data.shape[0]
    
    print( badRows )
    print( 'Number of rows dropped:', rowCount, '\n' )
    return data

def cleanData(filename):
    # Opens the csv with data so it can be cleaned 
    data_file = openFile( filename )
    
    # Call function to remove missing values
    print( 'Missing Data for 2011 Permit data: ')
    data_file = removeMissing( data_file )
    
    

def main():
   collectData()
   cleanData(permits2010)
   cleanData(permits2018)
   
df_2010 = openFile(permits2010)
df_2018 = openFile(permits2018)
        
if __name__== "__main__" :
    main()