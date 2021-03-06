# Disaster Response Pipeline Project

## 1- Project Description:
This project aims at collecting data recieved from tweets during a certrain disaster, classifying this data based on its contents,
so that it is used to provide the required assistance to people based on their circumstances during the disaster.

The code consists of scripts that collect data from two files: messages.csv and categories.csv, combines them,
cleans them and build a classification model based on this data. The model is then deployed locally to a flask app.

## 2- Packages used:

NLTK <br>
re

## 3- Script Files:

- process_data.py : Contains the script for ingesting, combining and cleaning the data
 To run it type the following command in the command line in the Data Folder Directory:
 python process_data.py disaster_messages.csv disaster_categories.csv DataBaseName.db 
 
 Rename DataBaseName with your prefered database name

- train_classifier.py : Contains the script for training, evaluating and saving the model to a pickle file
 To run it type the following command in the command line in the Models Folder Directory:
  python train_classifier.py DataBaseName.db  Classifier.pkl 
 <br>
 Rename Classifier with your prefered classifier name
<br>
<br>

- run.py: Contains the Flask web App

To run it type following command in the command line in the App Folder Directory: python run.py

Go to http://0.0.0.0:3000/
<br>
<br>
## 4- Other files and project layout:

app <br>
| - template <br>
| |- master.html # main page of web app <br>
| |- go.html # classification result page of web app <br>
|- run.py # Flask file that runs app <br>
data <br>
|- disaster_categories.csv # data to process <br>
|- disaster_messages.csv # data to process <br>
|- process_data.py <br>
|- DisasterResponse.db # database to save clean data to  <br>
models <br>
|- train_classifier.py <br>
|- classifier2.pkl # saved model <br>
README.md
