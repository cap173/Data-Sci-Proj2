from scipy.stats import ttest_ind
import pandas as pd

census2000_file = 'census_2000_CLEAN.csv'
census2010_file = 'census_2010_CLEAN.csv'

def openFile(filename):
    # Creation of pandas dataframe
    myData = pd.read_csv(filename, sep=',', encoding='latin1')
    return myData

# Calculate percentage of white people per tract (200)
# Put those results in a new column
def ratio2000(myData):

    myData['PERCENT_WHITE2000'] = myData['WHITE']/myData['TOTAL00']

    return myData

# Calculate percentage of white people per tract (2010)
# Put those results in a new column
def ratio2010(myData):

    myData['PERCENT_WHITE2010'] = myData['Pop of 1 race: White'] / myData['Total Population']

    #print(myData['PERCENT_WHITE2010'])

    return myData

#calculate ttest result
def ttest(census2000, census2010):

    print(ttest_ind(census2000.dropna()['PERCENT_WHITE2000'], census2010.dropna()['PERCENT_WHITE2010']))


def main():

    #from data to dataframes
    census_2000 = openFile(census2000_file)
    census_2010 = openFile(census2010_file)

    #creation of new column that contains percentage of white people
    census_2000 = ratio2000(census_2000)
    census_2010 = ratio2010(census_2010)

    #ttest results
    ttest(census_2000, census_2010)



if __name__ == "__main__":
    main()