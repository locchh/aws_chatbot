import os
import csv

FILE_PATH = './notebooks/questions.csv'

questions = []

# Open the CSV file
with open(FILE_PATH, newline='') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile, delimiter=',')
    
    # Iterate over the rows and print them
    for row in csvreader:
        questions.append(row[0])

# remove first row
questions = questions[1:]

print(questions[0])