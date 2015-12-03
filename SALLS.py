import csv

with open("SALLS.csv") as csvfile:
	reader1 = csv.reader(csvfile)
	data = reader1.split()
	new_data = data[0:3:2]

print(new_data)




