import sys
# import libraries
import numpy as np
import pandas as pd
import sqlite3
import re

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sqlalchemy import create_engine

from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC

import pickle


def load_data(database_filepath):
    """
    This function loads the data from the Database and saves it to independent variable x
    and labels Y 
    
    Returns : x , Y  and the column names
    
    """
    
    database_file='sqlite:///'+ database_filepath
    engine = create_engine(database_file)
   
    df = pd.read_sql('SELECT * FROM disaster_table', engine)

    x = df.message
    Y = df.iloc[:,3:]
    category_names=Y.columns.tolist()
    
    return x,Y, category_names


def tokenize(text):
    """    
    This function detects urls in text and replaces it with a specific string
    divides the string to words
    converts words to its bare minimum form
    and removes formatting
    """
    
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text.replace(url,'url_placeholder')
    tokens=word_tokenize(text)
    lemmatizer=WordNetLemmatizer()
    
    clean_tokens=[]
    for token in tokens:
        clean_tokens.append(lemmatizer.lemmatize(token).lower().strip())
    return clean_tokens


def build_model():
    """
    This function builds the pipeline that includes transofrmations and the model with its parameters
    It also uses a gridsearch object to find the best hyperparameters for the model
    """
    pipeline = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize)),
    ('tfidf', TfidfTransformer()),
    ('moc' , MultiOutputClassifier(AdaBoostClassifier()))])
    parameters ={
 
    'moc__estimator__n_estimators': [100,150],
    
    'moc__estimator__learning_rate':[0.8,1],
   }
    gridsearch = GridSearchCV(estimator=pipeline, cv=5, verbose=3, scoring='recall_micro',param_grid=parameters)
    
    
    return gridsearch


def evaluate_model(model, X_test, Y_test, category_names):
    """
    This function evaluates the percision, recall and F1 score for every class of the model
    """
    Y_pred_ar=model.predict(X_test)
    Y_pred=pd.DataFrame(Y_pred_ar)
    Y_test=pd.DataFrame(Y_test)
    
    
    print(classification_report(Y_test, Y_pred, target_names = category_names))


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))
    


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')
        
# To run the file copy paste the below line while replacing the last two arguments to be your Database Name and the prefered pickle file name        
# python train_classifier.py DisasterResponse.db  Classifier2.pkl

if __name__ == '__main__':
    main()