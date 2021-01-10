import csv

#with open('dev_disp', 'r') as csv_file:
with open(r'C:\Users\singhs113\titanic.csv') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
        print(line)