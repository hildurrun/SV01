import csv
import string
import numpy as np
from collections import Counter


#FALL SEM TEKUR NAUÐSYNLEGAR UPPLÝSINGAR ÚR VIÐEIGANDI SKRÁ, VINNUR ÚR UPPLÝSINGUM OG SKILAR NUMPY FYLKI
def data_to_numpy(filename):
	f = open(filename)
	csv_f = csv.reader(f, delimiter=';')
	data = list(csv_f)
	f.close()

	#BY TIL TVO LISTA UR CSV SKRA MED NAUDSYNLEGUM UPPLYSINGUM
	years = []
	income = []

	for row in data[1:]:
		year = row[0]
		income_per_year = row[3]

		years.append(int(year))
		income.append(income_per_year)

	#BREYTI '..'' I NULL SVO HAEGT SE AD GERA INT NUMPY FYLKI UR NIDURSTODUM
	X= '..'
	Y='0'

	while X in income:
		income.insert(income.index(X), Y)
		income.pop(income.index(X))


	#GET NU GERT INCOME LISTANN SEM HEILTOLUBREYTUR ÞVI PUNKTUM HEFUR VERID BREYTT I NÚLL
	income = [int(i) for i in income]

	#SPLAESI ARUM OG LAUNUM SAMAN I NUMPY FYLKI
	year_and_income = np.column_stack((years, income))

	#EYDI UT LÍNUM THAR SEM ENGIN LAUN ERU TIL STADAR, Þ.E. ÞEGAR LAUN = 0 SVO ÞAÐ SKEKKI EKKI MEÐALTALIÐ
	updated_year_and_income = year_and_income[np.all(year_and_income != 0, axis=1)]		

	#FINNA FJOLDA VERKFRÆÐISTÉTTA A ARI
	unique,counts = np.unique(updated_year_and_income[:,0], return_counts=True)
	count_per_years = np.asarray((unique,counts)).T

	all_years = []
	avg_income_years = []
	index=0

	#TVEIR NYJIR LISTAR MED AVG LAUNUM A ARI MIDAD VIÐ ÁKVEÐINN FJOLDA VERKFRÆÐISTÉTTA Á ÁRI
	for row in range(len(count_per_years)):
		one_year = count_per_years[row][0]
		avg_income_year =round(np.mean(updated_year_and_income[index:index+(count_per_years[row][1]),1]))
		index = index+count_per_years[row][1]

		all_years.append(int(one_year))
		avg_income_years.append(int(avg_income_year))

	#SPLAESI LISTUNUM TVEIMUR I NUMPY FYLKI
	years_income_to_numpy =np.column_stack((all_years, avg_income_years))

	return years_income_to_numpy,count_per_years


#FALL SEM NOTAR SKRÁ YFIR VÍSITOLUHÆKKUN Í PRÓSENTUM FYRIR HVERN MÁNUÐ Á TÍMABILINU OKKAR.
#STYÐJUMST VIÐ ÞESSA PRÓSENTUHÆKKUN TIL ÞESS AÐ FINNA LAUN Á ÁRI MIÐAÐ VIÐ VÍSITÖLUNA OG LAUN ÁRSINS Á UNDAN.
def index_function(filename,income,year):

	f = open(filename)
	csv_f = csv.reader(f, delimiter=';')
	data = list(csv_f)
	f.close()

	#BY TIL TVO LISTA UR CSV SKRA MED NAUDSYNLEGUM UPPLYSINGUM
	all_index= []

	for row in data[1:]:
		index = row[2]

		all_index.append(index)


	#BREYTI LISTANUM I FLOAT NUMPY LISTA/FYLKI
	index_np = np.array(all_index).astype(np.float)

	avg_index_per_year = []
	i=0
	months_in_year = 12

	#NYR NUMPY LISTI MED MEDALVISITOLUM A ARI
	for row in range(len(year)):
		avg_index_year =np.mean(index_np[i:months_in_year+i])
		i = months_in_year + i

		avg_index_per_year.append(float(avg_index_year))

	#FÆKKA AUKASTAFINA NIÐUR Í TVO
	avg_index_per_year = np.around(avg_index_per_year,decimals=2)

	#NÝIR LISTAR BÚNIR TIL ÚT FRÁ VÍSITOLULISTANUM, EN ÞESSIR INNIHALDA ÁRIN OG SVO LAUN SAMKV. VÍSITÖLU
	avg_income_index = []
	all_years = []

	for row in range(len(year)):
		if row is 0: #GETUM EKKI FUNDIÐ LAUN ÚT FRÁ VÍSITOLU FYRSTA ÁRIÐ SVO SETJUM LAUNIN ÞAR = 0
			avg_income_oneyear = 0
			one_year = year[0][0]
		else:	
			avg_income_oneyear =round((((avg_index_per_year[row])/100)+1)*(income[row-1][1]))
			one_year = year[row][0]

		avg_income_index.append(int(avg_income_oneyear))
		all_years.append(int(one_year))

	#SMELLUM ÖLLU SAMAN Í EITT NUMPY FYLKI
	years_income_index_numpy=np.column_stack((all_years, avg_income_index))
	
	return years_income_index_numpy

#NOTUM ÞETTA FALL TIL ÞESS AÐ VINNA ÚR UPPLÝSINGUM ÚR CSV SKRA SEM INNIHELDUR UPPLÝSINGAR UM HINN ALMENNA STJÓRNENDA
def data_to_numpy_overall(filename):

	f = open(filename)
	csv_f = csv.reader(f, delimiter=';')
	data = list(csv_f)
	
	#DROGUM ÚT NAUÐSYNLEGAR UPPLÝSINGAR OG SPLÆSUM Í TVO LISTA
	years = []
	income = []

	for row in data[1:]:
		one_year = row[0]
		income_per_year= row[3]

		years.append(int(one_year))
		income.append(int(income_per_year))

	#SKILUM LISTUNUM SEM EINU NUMPY FYLKI
	year_and_income_numpy = np.column_stack((years,income))

	return year_and_income_numpy

#FALL SEM SKILAR MISMUN Á LAUNUM SAMKV. HAGSTOFU OG LAUNUM SAMKV. VÍSITOLU OG ÞANNIG FINNUM VIÐ RAUNVERULEGA LAUNAHÆKKUN MILLI ÁRA
def real_increase(avg_income,avg_income_index,years):
	
	income_increase_overall = []

	#NIÐURSTÖÐUR SETTAR Í LISTA
	for row in range(len(years)):
		if row is 0:
			income_increase = 0
		else:
			income_increase = (avg_income[row][1]) - (avg_income_index[row][1])

		income_increase_overall.append(int(income_increase))

	#LISTA BREYTT Í NUMPY LISTA/FLKI
	income_increase_overall_np = np.array(income_increase_overall).astype(np.int)
	return income_increase_overall_np


#FALLIÐ FINNUR MESTU RAUNHÆKKUN FYRIR HVERN FLOKK OG PRENTAR ÚT NIÐURSTÖÐUNA
def get_max(pandasinfodata,KK_KVK,KK,KVK):
	print('Hvaða ár var mesta raunhækkun á launum?')

	highest_income_change = pandasinfodata.max()

	highest_income_overall = pandasinfodata[KK_KVK].argmax()
	highest_income_KK = pandasinfodata[KK].argmax()
	highest_income_KVK = pandasinfodata[KVK].argmax()

	print('Árið', highest_income_overall, 'var',KK_KVK, highest_income_change[0],'í þúsundum króna.')
	print('Árið', highest_income_KK, 'var',KK, highest_income_change[1],'í þúsundum króna.')
	print('Árið', highest_income_KVK, 'var',KVK, highest_income_change[2],'í þúsundum króna.')


#FALLIÐ FINNUR MESTU RAUNLAEKKUN FYRIR HVERN FLOKK OG PRENTAR ÚT NIÐURSTÖÐUNA
def get_min(pandasinfodata,KK_KVK,KK,KVK):
	print('\n')
	print('Hvaða ár var mesta raunlækkun á launum?')

	lowest_income_change = pandasinfodata.min()

	lowest_income_overall = pandasinfodata[KK_KVK].argmin()
	lowest_income_KK = pandasinfodata[KK].argmin()
	lowest_income_KVK = pandasinfodata[KVK].argmin()
	print('Árið', lowest_income_overall, 'var',KK_KVK, lowest_income_change[0],'í þúsundum króna.')
	print('Árið', lowest_income_KK, 'var',KK, lowest_income_change[1],'í þúsundum króna.')
	print('Árið', lowest_income_KVK, 'var',KVK, lowest_income_change[2],'í þúsundum króna.')


#FALLIÐ FINNUR HLUTFALL Á RAUNHAEKKUN Á LAUNUNUM MILLI KK OG KVK OG PRENTAR ÚT HLUTFALLIÐ Í PRÓSENTUM
def increase_prosent(KK_increase,KVK_increase):
	print('\n')
	total_increase_KK = np.sum(KK_increase)
	total_increase_KVK = np.sum(KVK_increase)

	if total_increase_KVK > total_increase_KK:
		increase_prosent_KVK = ((total_increase_KVK/total_increase_KK)-1)*100
		increase_prosent_KVK = np.around(increase_prosent_KVK,decimals=2)
		print('Laun kvenna hækkuðu',increase_prosent_KVK,'% meira heldur en laun karla á tímabilinu 1998-2014')

	elif total_increase_KVK < total_increase_KK:
		increase_prosent_KK = ((total_increase_KK/total_increase_KVK)-1)*100
		increase_prosent_KK = np.around(increase_prosent_KK,decimals=2)
		print('Laun karla hækkuðu',increase_prosent_KK,'% meira heldur en laun kvenna á tímabilinu 1998-2014')


