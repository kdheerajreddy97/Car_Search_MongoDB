[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11305281&assignment_repo_type=AssignmentRepo)

Project title: NoSQL Ninjas - Craiglist search using MongoDB and FastAPI

MongoDB Group Project:

Project Description: This application provides the user with the ability to search for cars from the Craigslist database. 
                     The user can search for cars based on the Manufacturer or in and around a particular location of 5kms radius.

Team Members:
Dheeraj Reddy Kukkala - dk8499@rit.edu
Shreya Pramod - sp3045@rit.edu
Mayur Reddy Sangepu - ms7483@rit.edu

In this project we used below tech stack:
1. Fast API web server application - Python - To get the data from the user to the backend - We used this because it is a popular choice for developing web applications and can handle concurrent requests very well.
2. MongoDB - To store the data and images
3. HTML, CSS - To display the data to the user
4. JavaScript - To create the index - For creating 2D sphere index for location

Fast API Installation steps:
Commands:
pip install fastapi uvicorn motor
pip install Jinja2
pip install python-multipart

Other packages to install:
pip install pymongo
pip install Form
pip install requests



Cleaning the data:
1. The data we used is vechiles.csv
2. We cleaned the data using the python script: 'datasetPreprocessing.py'

Data cleaning steps:
datasetPreprocessing.py steps:
1. We used the pandas library to read the csv file
2. We used the pandas library to drop the columns which are not required
3. We used the pandas library to drop the rows - Drop rows with missing values in the columns 'lat', 'long', 'image_url', and 'description' using df.dropna(subset=...)
4. Then we saved the cleaned data into a new csv file - craiglist.csv

MongoDB Database loading steps:
1. Open terminal
2. Go to the project folder
3. Run the command in order to import the data: `mongoimport --db Craiglist --collection Cars --file craiglist.csv`

Image Extraction:
imageExtraction.py steps:
1.Import the necessary libraries: pandas, pymongo from MongoClient, gridfs, pprint from pprint, requests, and Image from PIL
2.Loadeded the GridFS with the image files
3.Due to issues with some of the image URL's we have loaded the GridFS with the 200 working images
4.We also added the deafult image

Issues faced:
1. We faced security issues while accessing certain URL's.


Setup MongoDB and Run the project:
1. Index creation:
    a. Open terminal
    b. type mongosh
    c. type use Craiglist
    b. type db.Cars.createIndex({description: "text"})

2. Run the Javascript file: 'createIndex.js'
    a. Open terminal
    b. Go to the project folder
    c. Run the command: `mongosh createIndex.js`

3. Run the python script: 'main.py'
    a. Open terminal
    b. Go to the project folder
    c. Run the command: `uvicorn main:app --reload`
    d. Open the browser and type the URL: http://localhost:8000  inorder to view the application.












