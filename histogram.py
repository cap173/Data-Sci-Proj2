import matplotlib.pyplot as plt
import pandas as pd

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


def scatter(df):

    #Creation of scatterplots

    df.plot.scatter(x='Vacant Housing Units', y='Pop of 1 race: Black')

    plt.savefig('VHPB.png')



    df.plot.scatter(x='FAGI_MEDIAN_2010', y='Vacant Housing Units')

    plt.savefig('FTVH.png')


    df.plot.scatter(x='Pop of 1 race: Black', y='FAGI_MEDIAN_2010')

    plt.savefig('PBFT.png')


    plt.show()


def main():

    census_2010 = openFile(census2010_file)

    histogram(census_2010)

    scatter(census_2010)


if __name__ == "__main__":
    main()