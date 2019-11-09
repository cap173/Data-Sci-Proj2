#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 00:34:46 2019

@author: aleidaolvera
"""

# Import all your libraries.
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# calculate the accuracy score of the model
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
#  model the Gaussian Navie Bayes classifier
from sklearn.naive_bayes import GaussianNB
#  model the Random Forest classifier
from sklearn.ensemble import RandomForestClassifier

######################################################
# Validation Check for Gaussian and Random Forest
######################################################

def validation_check(X_train, Y_train, X_validate, Y_validate):
        # GaussianNB Validation Check
        print('Validation Check for GaussianNB')
        gnb = GaussianNB()
        gnb.fit(X_train, Y_train)
        gnb_predictions = gnb.predict(X_validate)
        
        print(accuracy_score(Y_validate, gnb_predictions))
        print(confusion_matrix(Y_validate, gnb_predictions))
        print(classification_report(Y_validate, gnb_predictions))
        
        # Random Forest Validation Check
        print('Validation Check for Random Forest')
        rf = RandomForestClassifier(n_estimators=50)
        rf.fit(X_train, Y_train)
        rf_predictions = rf.predict(X_validate)
        
        print(accuracy_score(Y_validate, rf_predictions))
        print(confusion_matrix(Y_validate, rf_predictions))
        print(classification_report(Y_validate, rf_predictions))

######################################################
# Run NB and RF over Data
######################################################
def run_nb_rf(df, categories):
    # set up for training model
    new_df = df[categories]
    valueArray = new_df.values
    X = preprocessing.normalize(valueArray[:, 1:4])
    Y = valueArray[:, 0]
    test_size = 0.30
    seed = 7
    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=test_size, random_state=seed)
    num_folds = 10
    scoring = 'accuracy'
    models = []
    models.append(('GNB', GaussianNB()))
    models.append(('RF', RandomForestClassifier(n_estimators=50)))
    
    # evaluate models, then add results to array
    # print the accuracy results
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
        
    validation_check(X_train, Y_train, X_validate, Y_validate)
    
######################################################
# Load Data
######################################################
def file_to_df( filename ):
    myData = pd.read_csv( filename , sep=',', encoding='latin1')
    return myData

def main():
#   census2000 = 'census_2000_CLEAN.csv'
    census2010 = 'census_2010_CLEAN.csv'
#   dfc2000 = file_to_df(census2000)
    dfc2010 = file_to_df(census2010)
    cat_c2010 = ['BIN_INCOME_CH_2005_2010', 'NEIGHBORHOODCLUSTER', 'POPDENSITY', 'FAGI_MEDIAN_2010', 'INCOME_LEVEL_2010']
    cat_c2015 = ['BIN_INCOME_CH_2010_2015', 'NEIGHBORHOODCLUSTER', 'POPDENSITY', 'FAGI_MEDIAN_2015', 'INCOME_LEVEL_2015']
    run_nb_rf(dfc2010, cat_c2010)
    run_nb_rf(dfc2010, cat_c2015)

if __name__ == '__main__':
    main()


