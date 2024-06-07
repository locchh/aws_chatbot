'''
python3 utils/convert_csv.py resource/exams/Exam1.txt
'''

import os
import sys
import csv

def remove_index(current_question):
    for i in range(10):
        if current_question[i] == '.':
            current_question = current_question[i+1:]
            break
    current_question = current_question.strip()
    return current_question

if __name__ == "__main__":

    # Get file path
    FILE_PATH = sys.argv[1]
    print('FILE_PATH=',FILE_PATH)
    file_name = os.path.basename(FILE_PATH)
    file_name = file_name.split('.')[0]
    csv_file_path = os.path.join(os.path.dirname(FILE_PATH),file_name+'.csv')

    # Read content
    with open(FILE_PATH) as f:
        content = f.read()

    # Split to element
    questions = content.split("\n\n")
    print('Total questions=',len(questions))

    # Clear all
    prepocessed_questions = [remove_index(q) for q in questions]

    
    # Write the list to the CSV file with a header
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["question"])
        # Write the text rows
        for question in prepocessed_questions:
            writer.writerow([question])

    print(f"List of text has been written to {csv_file_path}")


