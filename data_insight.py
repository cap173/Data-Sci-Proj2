#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 6 21:20:00 2019

@author: aleidaolvera
"""

import pandas as pd

def file_to_df( filename ):
    myData = pd.read_csv( filename , sep=',', encoding='latin1')
    return myData

'''
Determine the mean (mode if categorical), median, and standard deviation of at least 10
attributes in your data sets. Use Python to generate these results and use the project
report to show and explain each. 
'''

def basic_statistical_analysis(df, cat_name):
    print('Basic Statistical Analysis of ' + str(cat_name))
    # mean
    print('Mean: ' + str(round(df[cat_name].mean(), 2)))
    # media
    print('Median: ' + str(round(df[cat_name].median(), 2)))
    # standard dev
    print('Standard Dev: ' + str(round(df[cat_name].std(), 2)))
    
def cat_statistical_analysis(df, cat_name):
    print('Categorical Analysis of ' + str(cat_name))
    print('Mode: ' + str(df[cat_name].mode()))
    

def main():
    permits2010 = 'permits_2010_CLEAN.csv'
    permits2018 = 'permits_2018_CLEAN.csv'
    census2000 = 'census_2000_CLEAN.csv'
    census2010 = 'census_2010_CLEAN.csv'
    dfc2000 = file_to_df(census2000)
    dfc2010 = file_to_df(census2010)
    dfp2010 = file_to_df(permits2010)
    dfp2018 = file_to_df(permits2018)
    
    
    print('----- Analysis of 2000 Census Data')
    basic_statistical_analysis(dfc2000, 'POPDENSITY')
    basic_statistical_analysis(dfc2000, 'TOTAL')
    '''
    TOTAL HOUSING UNITS Analysis
        We were able to detect that this column of code is riddled with faulty data.
        We came to this conclusion because of the low numbers that were returned from our
        initial statistical analysis. For this reason, we have chosen not to analyze the
        Total Number of Housing Units
    '''
    basic_statistical_analysis(dfc2000, 'TOTHOUSEUN')
    basic_statistical_analysis(dfc2000, 'WHITE')
    
    print('----- Analysis of 2010 Census Data')
    basic_statistical_analysis(dfc2010, 'POPDENSITY')
    basic_statistical_analysis(dfc2010, 'Total Population')
    '''
    TOTAL HOUSING UNITS Analysis
        The 2000 Census Data for total housing units was corrupted, but this data set was not.
        Unfortunately, because the 2000 Census Data's information is vital to our analysis,
        we have decided to drop this variable from our future analysis.
    '''
    basic_statistical_analysis(dfc2010, 'Total Housing Units')
    basic_statistical_analysis(dfc2010, 'Pop of 1 race: White')
    
    print('----- Analysis of 2010 Building Permit Data')
    basic_statistical_analysis(dfp2010, 'FEES_PAID')
    cat_statistical_analysis(dfp2018, 'PERMIT_SUBTYPE_NAME')
    print('----- Analysis of 2018 Building Permit Data')
    basic_statistical_analysis(dfp2018, 'FEES_PAID')
    cat_statistical_analysis(dfp2018, 'PERMIT_SUBTYPE_NAME')

if __name__== "__main__" :
    main()