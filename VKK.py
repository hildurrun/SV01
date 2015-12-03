import csv

with open("VKK.csv") as csvfile:
	reader = csv.reader(csvfile)
	list1 = list(reader)

print(list1)

csvfile.close()
