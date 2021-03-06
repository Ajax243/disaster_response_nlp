import sys
# import libraries
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import re


def load_data(messages_filepath, categories_filepath):
    """
    This function takes the messages and the categories filepath and returns them in a combined DataFrame
    """
    
    # load messages dataset
    messages = pd.read_csv(messages_filepath)

    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    
    # merge datasets
    df = pd.concat([messages,categories],axis=1 , sort=False)
    df=df[['id','message','original','genre','categories']]
    
    return df


def clean_data(df):
    """
    This function takes the DataFrame and cleans it and makes it ready to be ingested by the ML algorithm
    """
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';',expand= True)
    
    row = categories.iloc[0,:]

    # use this row to extract a list of new column names for categories.
    category_colnames = [x.split('-')[0] for x in row]
    print(category_colnames)

    # rename the columns of `categories`
    categories.columns = category_colnames
    

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x.split('-')[1])
        # convert column from string to numeric
        categories[column] = categories[column].replace('nan',0)
        categories[column] = categories[column].astype(int)
    categories['related']=categories['related'].replace(2,1)
    
    # drop rows with no labels
    categories=categories.loc[~(categories==0).all(axis=1)]
    
    # drop the original categories column from `df`
    df=df[['message','genre']]
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis=1)
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # drop nulls
    df.dropna(inplace=True)
    df=df.reset_index()
    
    return df


def save_data(df, database_filename):
    """
    This function saves the clean DataFrame as a table in a Database, and replaces the table if it already exists
    """
    #Save Dataframe to a database
    database_file='sqlite:///'+database_filename
    engine = create_engine(database_file)
    
    df.to_sql('disaster_table', engine, index=False, if_exists='replace' )  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')
        
# To run the file copy paste the below line while replacing the last argument with your prefered Database Name
# python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db
        
if __name__ == '__main__':
    main()