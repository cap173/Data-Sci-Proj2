import pandas as pd
import numpy as np
import csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

census2000_file = 'census_2000_CLEAN.csv'
census2010_file = 'census_2010_CLEAN.csv'


# Opens CSV file and returns pandas dataframe
def file_to_df( filename ):
    myData = pd.read_csv( filename , sep=',', encoding='latin1')
    return myData

# Creates a new column in each datafram that takes the total number of White
# people recorded and divdes it by the total population in that area.
def createNewVar2000( census2000 ):
    # Create variable for census2000 data
    # We found a row wehre TOTAL == 0 which is making %WHITE NaN and I tried 
    # this method and it didn't work so I decided to manually remove the row
    #census2000['TOTAL'].replace(0, np.nan, inplace=True)
    #census2000.dropna( axis='columns' )
    census2000 = census2000.drop( census2000.index[59] )
    
    census2000['%WHITE'] = census2000['WHITE'] / census2000['TOTAL']
    census2000['%WHITE'] = census2000['%WHITE'].round( decimals=3 )

    return census2000
 
def createNewVar2010( census2010 ):    
    # Create variable for census2010 data
    census2010['%WHITE'] = census2010['Total Non-Minority Population (White Not Hispanic)'] / census2010['Total Population']
    return census2010 
    
def tTest( census2000, census2010 ):
    # Perform t-test for Census 2000 data
    # Get values of %WHITE and FAGI_MEDIAN_2005 in lists
    x_WHITE = census2000['%WHITE'].to_numpy().reshape((-1,1))
    y_FAGI = census2000['FAGI_MEDIAN_2005'].to_numpy()
    
    
    # Create linear regression and 
    model = LinearRegression().fit( x_WHITE, y_FAGI )
    r2 = model.score( x_WHITE, y_FAGI )
    print('R-squared score for 2000:', r2 )
    
    # Perform t-test for Census 2010 data
    # Get values of %WHITE and FAGI_MEAN_2005 in lists
    x_WHITE = census2010['%WHITE'].to_numpy().reshape((-1,1))
    y_FAGI = census2010['FAGI_MEDIAN_2010'].to_numpy()
    
    
    model = LinearRegression().fit( x_WHITE, y_FAGI )
    r2 = model.score( x_WHITE, y_FAGI )
    print('R-squared score for 2010:', r2, '\n' )

def classifier( census2000, census2010 ):
    # Create subset of Census 2000 data to train to classify neighborhood cluster 
    myData2000 = census2000[['TOTAL','WHITE','BLACK','AMERIND','ASIAN','HISPANIC','FAGI_TOTAL_2005',
             'FAGI_MEAN_2005', 'NEIGHBORHOODCLUSTER']]
    # Separate training and final validation data sets. 
    valueArray = myData2000.values
    X = valueArray[:, 0:9]
    Y = valueArray[:, 8]
    test_size = 0.20
    seed = 7
    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=test_size, random_state=seed)

    num_folds = 10
    seed = 7
    scoring = 'accuracy'    

    # Add each algorithm and its name to the model array
    models = []
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('DT', DecisionTreeClassifier()))
    
    # Evaluate each model, add results to a results array,
    # Print the accuracy results (remember these are averages and std
    results = []
    names = []
    print('Models for Census 2000:')
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
        
        model.fit(X_train, Y_train)
        predictions = model.predict(X_validate)
        
        print( name, 'Validation:')
        print(accuracy_score(Y_validate, predictions))
        print(confusion_matrix(Y_validate, predictions), '\n')


    
    # Create subset of Census 2010 data to train to classify neighborhood cluster 
    myData2010 = census2010[['Total Population','Total Non-Minority Population (White Not Hispanic)',
             'Total Hispanic Population','Not Hispanic Pop of 1 race: Black',
             'Not Hispanic Pop of 1 race: American Indian Alaskan',
             'Not Hispanic Pop of 1 race: Asian','Not Hispanic Pop of 1 race: Other Race',
             'FAGI_TOTAL_2010','FAGI_MEDIAN_2010', 'NEIGHBORHOODCLUSTER']]
    # Separate training and final validation data sets. 
    valueArray = myData2010.values
    X2 = valueArray[:, 0:9]
    Y2 = valueArray[:, 9]
    X_train2, X_validate2, Y_train2, Y_validate2 = train_test_split(X2, Y2, test_size=test_size, random_state=seed)
    print('Models for Census 2010:')
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train2, Y_train2, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg, '\n')
        
        model.fit(X_train2, Y_train2)
        predictions = model.predict(X_validate2)
        
        print( name, 'Validation:')
        print(accuracy_score(Y_validate2, predictions))
        print(confusion_matrix(Y_validate2, predictions), '\n')
    


def main():
    census2000 = file_to_df( census2000_file )
    census2010 = file_to_df( census2010_file )
    census2000 = createNewVar2000( census2000 )
    census2010 = createNewVar2010( census2010 )
    
    tTest( census2000, census2010 )
    classifier( census2000, census2010 )
    
if __name__ == "__main__":
    main()