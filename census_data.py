import requests
import csv
import json
import pandas as pd

urlFor2000 = 'https://opendata.arcgis.com/datasets/f88d947d0ba945b688e00a46d6cbcd6c_9.csv'
csv2000 = 'census_2000.csv'
urlFor2010 = 'https://opendata.arcgis.com/datasets/6969dd63c5cb4d6aa32f15effb8311f3_8.csv'
csv2010 = 'census_2010.csv'
clean2000 = open( 'census_2000_CLEAN.csv', 'w' )
clean2010 = open( 'census_2010_CLEAN.csv', 'w' )

def collectData():
   # Request 2000 data from API and save it into a csv file
   request = requests.get( urlFor2000 )
   outFile = open( csv2000, 'wt' )
   outFile.write( request.text )
   
   # Request 2010 data from API and save it into a csv file
   request = requests.get( urlFor2010 )
   outFile = open( csv2010, 'wt' )
   outFile.write( request.text )
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

def rename_census_columns(df):
    df = df.rename(columns={"P0010001": "Total Population", "P0010002": "Total Pop of 1 Race",
                             "P0010003": "Pop of 1 race: White", "P0010004": "Pop of 1 race: Black",
                             "P0010005": "Pop of 1 race: American Indian Alaskan",
                             "P0010006": "Pop of 1 race: Asian",
                             "P0010007": "Pop of 1 race: Native Hawaiian Pacific Islander",
                             "P0010008": "Pop of 1 race: Other Race", "OP000001": "Pop 2 or more races: Black and",
                             "OP000002": "Pop 2 or more races: American Indian Alaskan and",
                             "OP000003": "Pop 2 or more races: Asian and",
                             "OP000004": "Pop 2 or more races: Native Hawaiian Pacific Islander and",
                             "P0020002": "Total Hispanic Population",
                             "P0020005": "Total Non-Minority Population (White Not Hispanic)",
                             "P0020006": "Not Hispanic Pop of 1 race: Black",
                             "P0020007": "Not Hispanic Pop of 1 race: American Indian Alaskan",
                             "P0020008": "Not Hispanic Pop of 1 race: Asian",
                             "P0020009": "Not Hispanic Pop of 1 race: Native Hawaiian Pacific Islander",
                             "P0020010": "Not Hispanic Pop of 1 race: Other Race",
                             "OP00005": "Not Hispanic Pop 2 or more races: Black and",
                             "OP00006": "Not Hispanic Pop 2 or more races: American Indian Alaskan and",
                             "OP00007": "Not Hispanic Pop 2 or more races: Asian and",
                             "OP00008": "Not Hispanic Pop 2 or more races: Native Hawaiian Pacific Islander and",
                             "P0030001": "Total Pop 18+", "P0030003": "18+ Pop 1 race: White",
                             "P0030004": "18+ Pop 1 race: Black", "P0030005": "18+ Pop 1 race: American Indian Alaskan",
                             "P0030006": "18+ Pop 1 race: Asian", "P0030007": "18+ Pop 1 race: Native Hawaiian Pacific Islander",
                             "P0030008": "18+ Pop 1 race: Other race", "OP00009": "18+ Pop 2 or more races: Black and",
                             "OP00010": "18+ Pop 2 or more races: American Indian Alaskan and",
                             "OP00011": "18+ Pop 2 or more races: Asian and",
                             "OP00012": "18+ Pop 2 or more races: Native Hawaiian Pacific Islander",
                             "P0040002": "Hispanic 18+ Pop", "P0040005": "Non-Minority 18+ Pop (White Non-Hispanic)",
                             "P0040006": "Not Hispanic 18+ Pop 1 race: Black",
                             "P0040007": "Not Hispanic 18+ Pop 1 race: American Indian Alaskan",
                             "P0040008": "Not Hispanic 18+ Pop 1 race: Asian",
                             "P0040009": "Not Hispanic 18+ Pop 1 race: Native Hawaiian Pacific Islander",
                             "P0040010": "Not Hispanic 18+ Pop 1 race: Other race",
                             "OP000013": "Not Hispanic 18+ Pop 2 or more races: Black and",
                             "OP000014": "Not Hispanic 18+ Pop 2 or more races: American Indian Alaskan and",
                             "OP000015": "Not Hispanic 18+ Pop 2 or more races: Asian and",
                             "OP000016": "Not Hispanic 18+ Pop 2 or more races: Native Hawaiian Pacific Islander and",
                             "H0010001": "Total Housing Units",
                             "H0010002": "Occupied Housing Units",
                             "H0010003": "Vacant Housing Units"})
    return df

def bin_census_data(df, cat_name, year):
    income_cat = 'INCOME_LEVEL_' + str(year)
    df[income_cat] = df[cat_name].apply(lambda x: 'LOW_INCOME' if x <= 30000 else ('MID_INCOME' if x <= 65000 else ('MID_HIGH_INCOME' if x < 100000 else 'HIGH_INCOME')))

def tract_to_cluster(df, cat_name):
    clusters = {
                '1': [39, 38, 40.02, 40.01, 41],
                '2': [30, 32, 31, 29, 28.01, 27.01, 27.02, 28.02, 37, 36],
                '3': [34, 35, 44, 43],
                '4': [1, 2.02, 2.01],
                '5': [108, 57.02, 57.01, 56, 55],
                '6': [107, 53.02, 53.01, 54.01, 54.02, 42.02, 42.01],
                '7': [52.01, 50.01, 50, 50.02, 49.02, 49.01, 48.02, 48.01],
                '8': [101, 51, 52.02, 58, 47.01, 47, 47.02, 59],
                '9': [62.01, 62.02, 102, 110, 64, 105, 60.01, 60.02, 63.01, 61],
                '10': [15, 14.02, 14.01],
                '11': [11, 10.01],
                '12': [13.01, 12, 13.02],
                '13': [8.02, 8.01, 9.01, 9.02],
                '14': [3, 7.02, 7.01, 10.02],
                '15': [6, 5.01, 5.02, 4, 73.02],
                '16': [16, 103],
                '17': [17.01, 17.02, 19.02, 19.01, 18.04, 18.03, 22.01],
                '18': [20.01, 26, 20.02, 21.01, 21.02, 23.01, 24, 25.02, 25.01],
                '19': [95.05, 95.07, 95.08, 95.01, 22.02],
                '20': [95.04, 95.09, 95.03],
                '21': [23.02, 92.01, 92.04, 87.02, 87.01, 46, 33.02, 33.01, 92.03],
                '22': [93.01, 93.02, 91.02, 91.01],
                '23': [89.04, 89.03, 88.02, 88.04, 88.03],
                '24': [94, 111, 90],
                '25': [106, 85, 84.1, 79.01, 79.03, 80.01, 81, 83.02, 83.01],
                '26': [68.04, 68.01, 68.02, 69, 67, 82, 80.02, 66, 65, 70, 84.02, 84.01],
                '27': [71, 72],
                '28': [75.03, 75.04],
                '29': [96.01],
                '30': [96.02, 78.03],
                '31': [78.06, 78.09, 78.04, 78.08, 78.07],
                '32': [77.08, 96.04, 96.03, 77.03],
                '33': [99.03, 99.04, 99.06, 99.07, 77.07, 99.05],
                '34': [99.02, 99.01, 77.09, 76.01, 76.05],
                '35': [76.04, 76.03],
                '36': [75.02, 74.08],
                '37': [74.01, 74.06, 74.07],
                '38': [73.04, 74.09, 74.03, 74.04],
                '39': [109, 73.01, 98.07, 98.11, 98.10, 97, 98.02, 98.08, 98.06, 98.01, 104, 98.04, 98.03]
            }
    # flip keys and values to match tracts with clusters
    tracts = {new_k: old_k for old_k, old_v in clusters.items() for new_k in old_v}
    # map tracts to clusters
    df['NEIGHBORHOODCLUSTER'] = df[cat_name].map(tracts)

def extra_clean_up(df, year):

    if year == '2000':
        df['FEDTRACTNO'].round(2)
        tract_to_cluster(df, 'FEDTRACTNO')
        bin_census_data(df, 'FAGI_MEDIAN_2005', '2005')
    elif year == '2010':
        df['TRACT'] = df['TRACT'] * float(0.01)
        df['TRACT'] = df['TRACT'].round(2)
        tract_to_cluster(df, 'TRACT')
        # add pop density, which is present in 2000 census but not in 2010 census
        # formula is total_population / sq_miles
        df['POPDENSITY'] = df['Total Population'] / df['SQ_MILES']
        bin_census_data(df, 'FAGI_MEDIAN_2010', '2010')
        bin_census_data(df, 'FAGI_MEDIAN_2015', '2015')
        

def change_income(df2000, df2010):
    df2010['INCOME_CH_2005_2010'] = (df2010['FAGI_MEDIAN_2010'] - df2000['FAGI_MEDIAN_2005']) / df2000['FAGI_MEDIAN_2005']
    df2010['INCOME_CH_2010_2015'] = (df2010['FAGI_MEDIAN_2015'] - df2010['FAGI_MEDIAN_2010']) / df2010['FAGI_MEDIAN_2010']
    df2010['INCOME_CH_2005_2010'] = df2010['INCOME_CH_2005_2010'].round(2)
    df2010['INCOME_CH_2010_2015'] = df2010['INCOME_CH_2010_2015'].round(2)
    

def cleanData():
    # Opens the csv with data so it can be cleaned 
    data2000 = openFile( csv2000 )
    data2010 = openFile( csv2010 )
    
    # Call function to remove missing values
    print( 'Missing Data for 2000 Census data: ')
    data2000 = removeMissing( data2000 )
    print( 'Missing Data for 2010 Census data: ')
    data2010 = removeMissing( data2010 )
    data2010 = rename_census_columns(data2010)
    extra_clean_up(data2000, '2000')
    extra_clean_up(data2010, '2010')
    change_income(data2000,data2010)
    # round all values to 2 decimal places
    data2000 = data2000.round(2)
    data2010 = data2010.round(2)
    # Write cleaned data to a new file
    data2000.to_csv( clean2000 )
    data2010.to_csv( clean2010 )
    

def main():
   collectData()
   cleanData()
        
if __name__== "__main__" :
    main()