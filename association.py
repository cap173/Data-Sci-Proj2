import pandas as pd
from apyori import apriori


census2010_file = 'census_2010_CLEAN.csv'

def openFile(filename):
    # Creation of pandas dataframe
    myData = pd.read_csv(filename, sep=',', encoding='latin1')
    return myData

#reorganize our dataframe into a list of lists (to use with apriori algorithm)
def preprocess(df):


    #using the only relevant colums
    newdf = pd.DataFrame(columns=['NEIGHBORHOODCLUSTER', 'INCOME_LEVEL_2010'])

    newdf['NEIGHBORHOODCLUSTER'] = df['NEIGHBORHOODCLUSTER'].astype(str)
    newdf['INCOME_LEVEL_2010'] = df['INCOME_LEVEL_2010']

    records = newdf.values.tolist()
    return records


def rules(data):

    aR = apriori(data, min_support= 0.3, min_confidence=0.2, min_length=2)

    results = list(aR)

    print(results)


def main():

    census2010 = openFile(census2010_file)

    data = preprocess(census2010)

    print(data)

    rules(data)





if __name__ == "__main__":
    main()

