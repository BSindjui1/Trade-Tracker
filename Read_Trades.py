import csv

all_trades = []  #This makes an array that will store all trades

with open('trades.csv', newline='') as  csvfile:
     reader =csv.DictReader(csvfile)
     for row in reader:
        all_trades.append(row) # This adds each row of the .csv file to the list   

# print(all_trades)