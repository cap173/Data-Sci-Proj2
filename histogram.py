import csv
import pandas as pd
import numpy as np, math
import matplotlib.pyplot as plt
import pylab as pl
import pandas as pd

permits2010_file = 'permits_2010_CLEAN.csv'
permits2018_file = 'permits_2018_CLEAN.csv'

census2010_file = 'census_2010_CLEAN.csv'

def openFile(filename):
    # Creation of pandas dataframe
    myData = pd.read_csv(filename, sep=',', encoding='latin1')
    return myData

def histogram(df):

    #Creation of histograms

    VHU = df.hist(column="Vacant Housing Units")

    plt.savefig('VHU.png')

    BA = df.hist(column="Pop 2 or more races: Black and")

    plt.savefig('BA.png')

    TP = df.hist(column="Total Population")

    plt.savefig('TP.png')

    plt.show()


def main():

    permits_2010 = openFile(permits2010_file)
    print('For Permits 2010 Data:\n')
    print(permits_2010)

    census_2010 = openFile(census2010_file)
    histogram(census_2010)

    permits2018 = openFile(permits2018_file)
    print('For Permits 2018 Data:\n')
    print(permits2018)
    histogram(permits2018)


if __name__ == "__main__":
    main()