import csv
import pandas as pd
import numpy as np, math
import matplotlib.pyplot as plt
import pylab as pl
from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn import preprocessing, metrics, cluster
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_samples, silhouette_score

census2000_file = 'census_2000_CLEAN.csv'
census2010_file = 'census_2010_CLEAN.csv'

def openFile( filename ):
    # Opens CSV file and creates a pandas dataframe 
    myData = pd.read_csv( filename, sep=',', encoding='latin1')
    return myData


def fix2000( df ):
    # Remove columns of data that aren't useful numerical data
    # Keep columns that are of interest (population, demogrpahics, income)
    # NOTE FAGI ( Federal Adjusted Gross Income )
    df = df[['TOTAL','WHITE','BLACK','AMERIND','ASIAN','HISPANIC','FAGI_TOTAL_2005',
             'FAGI_MEAN_2005']]
    return df


    
def fix2010( df ):
    # Remove columns of data that aren't useful numerical data
    # Keep columns that are of interest (population, demogrpahics, income)
    # NOTE FAGI ( Federal Adjusted Gross Income )
    df = df[['Total Population','Total Non-Minority Population (White Not Hispanic)',
             'Total Hispanic Population','Not Hispanic Pop of 1 race: Black',
             'Not Hispanic Pop of 1 race: American Indian Alaskan',
             'Not Hispanic Pop of 1 race: Asian','Not Hispanic Pop of 1 race: Other Race',
             'FAGI_TOTAL_2010','FAGI_MEDIAN_2010']]
    return df 

def ward( df, framename ):
    # Creates numpy array with values 
    x = df.values
    
    # Clusters data from array
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    
    ward = AgglomerativeClustering(affinity='euclidean', compute_full_tree='auto',
                        connectivity=None, distance_threshold=None,
                        linkage='ward', memory=None, n_clusters=2,
                        pooling_func='deprecated').fit( normalizedDataFrame )
    cluster_labels = ward.labels_
    silhouette_avg = silhouette_score( normalizedDataFrame, cluster_labels)
    print('The average silhouette_score for Ward clustering is:', silhouette_avg, '\n' )
    
    # Create PCA projection for Ward clusters
    pca( normalizedDataFrame, cluster_labels, framename, 'Ward' )
    print('\n')
    
    
def km( df, framename ):
    # Preprocess all the data before employing kmeans algorithim
    x = df.values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    
    # Calculate silhouette score for different k's 
    for k in range( 3, 8 ):
        kmeans = KMeans(n_clusters=k)
        cluster_labels = kmeans.fit_predict(normalizedDataFrame) 
        silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
        print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    
    # Create PCA projection for K-Means clusters
    pca( normalizedDataFrame, cluster_labels, framename, 'K-Means' )
    print('\n')
    
def db( df, framename ):
    # Create numpy array with values
    x = df.values
    
    #Preprocess Data
    #stand_scaler = preprocessing.StandardScaler()
    #x_scaled = stand_scaler.fit_transform(x)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    
    # Calculate silhouette score using DBSCAN
    dbscan = cluster.DBSCAN( eps = .3 ).fit( normalizedDataFrame )
    cluster_labels = dbscan.labels_
    silhouette_avg = silhouette_score( normalizedDataFrame, cluster_labels)
    print('The average silhouette_score for DBSCAN with eps=.3 is:', silhouette_avg, '\n' )
    
    # Create PCA projection for DBSCAN clusters
    pca( normalizedDataFrame, cluster_labels, framename, 'DBSCAN' )
    print('\n')
    
    
def pca( normalizedDataFrame, cluster_labels, framename, clustname ):
    pca2D = decomposition.PCA(2)

    # Turn the Census data into two columns with PCA
    pca2D = pca2D.fit(normalizedDataFrame)
    plot_columns = pca2D.transform(normalizedDataFrame)
    
    # This shows how good the PCA performs on this dataset
    print(pca2D.explained_variance_)
    
    # Plot using a scatter plot and shade by cluster label
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    plt.title("2-dimensional scatter plot using PCA")
    
    # Write to file
    plt.savefig(framename+'_'+clustname+'_'+'pca2D.png')
    
    # Clear plot
    plt.clf()


def main():
    census2000 = openFile( census2000_file )
    print('For Census 2000 Data:\n' )
    census2000 = fix2000( census2000 )
    ward( census2000, 'census2000' )
    km( census2000, 'census2000' )
    db( census2000, 'census2000' )
    
    census2010 = openFile( census2010_file )
    print('For Census 2010 Data:\n' )
    census2010 = fix2010( census2010 )
    ward( census2010, 'census2010' )
    km( census2010, 'census2010' )
    db( census2010, 'census2010' )

    

if __name__== "__main__" :
    main()