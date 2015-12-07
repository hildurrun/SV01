import csv
import string
import numpy as np
import pandas as pd
from collections import Counter
import FOLL as F

#Skilgreinum numpy fylkja breytur fyrir völdu launaflokkana okkar, allar breytur innihalda ár og svo laun.
avg_year_income_overall = F.data_to_numpy_overall('SALLS.csv')
avg_year_income_KK,count_years_KK = F.data_to_numpy('VKK.csv')
avg_year_income_KVK,count_years_KVK = F.data_to_numpy('VKVK.csv')

#Skilgreinum numpy fylkja breytur fyrir völdu launaflokkana okkar, nú miðað við vísitölu neysluverðs.
income_basedOnIndex_KK = F.index_function('visitolur.CSV',avg_year_income_KK,count_years_KK)
income_basedOnIndex_KVK = F.index_function('visitolur.CSV', avg_year_income_KVK,count_years_KK)
income_basedOnIndex_overall = F.index_function('visitolur.CSV', avg_year_income_overall, count_years_KK)

#Skilgreinum numpy fylkja breytur fyrir völdu launaflokkana okkar, en breyturnar innihalda raunverulega hækkun á launum milli ára.
real_increase_overall =F.real_increase(avg_year_income_overall,income_basedOnIndex_overall,count_years_KK)
real_increase_KK = F.real_increase(avg_year_income_KK, income_basedOnIndex_KK,count_years_KK)
real_increase_KVK = F.real_increase(avg_year_income_KVK, income_basedOnIndex_KVK,count_years_KK)

#Setjum raunhækkanir nú í pandas töflu sem sýnir niðurstöðurnar best.

#Skilgreinum flokkana í dálkunum
A = 'Raunhaekkun á launum stjórnenda alls(KK/KVK)'
B = 'Raunhaekkun á launum KK í verkfr. stöðu'
C = 'Raunhaekkun á launum KVK í verkfr. stöðu'

columns = [A,B,C]
index = [avg_year_income_KK[:,0]] #Náum í öll árin úr þessari numpy breytu, hefðum getað valið nánast hvaða numpy breytu
#hér fyrir ofan enda innihalda þær nánast allar árin í fyrsta dálk.

data = {A:real_increase_overall,B:real_increase_KK,C:real_increase_KVK}
real_increase_pandasTable = pd.DataFrame(data,columns=columns, index=index)

#Skrifum pandas töflu beint út í csv skrá og opnum í excel til þess að plotta töfluna.
real_increase_pandasTable.to_csv('raunhaekkun.csv',encoding='utf-8')

#Fallid get_max finnur árið sem gefur mestu raunhaekkun fyrir hvern flokk fyrir sig og prentar út niðurstöður.
F.get_max(real_increase_pandasTable,A,B,C)

#Fallið min_max finnur árið sem gefur mestu raunlækkun fyrir hvern flokk fyrir sig og prentar út niðurstöður.
F.get_min(real_increase_pandasTable,A,B,C)

#Fallið haekkun_prosent finnur hlutfallslega prósentuhaekkun á launum á tímabilinu okkar milli KVK og KK.
F.increase_prosent(real_increase_KK,real_increase_KVK)


#Setjum nú laun stjórnenda í aðra pandas töflu sem sýnir þróunina á laununum ár hver.

#Skilgreinum flokkana á dálkum
A = 'Laun allra stjornenda (KK/KVK)'
B = 'Laun allra stjornenda (KK/KVK m.v. visitolubreytingu)'
C = 'Laun KK stjornenda i verkfr.stodu'
D = 'Laun KK stjornenda i verkfr.stodu (m.v. visitolubreytingu)'
E = 'Laun KVK stjornenda i verkfr.stodu'
F = 'Laun KVK stjornenda i verkfr.stodu (m.v. visitolubreytingu)'

index = [avg_year_income_KK[:,0]]
columns = [A, B, C, D, E, F]

data = {A:avg_year_income_overall[:,1],B:income_basedOnIndex_overall[:,1],C:avg_year_income_KK[:,1],D:income_basedOnIndex_KK[:,1],E:avg_year_income_KVK[:,1],F:income_basedOnIndex_KVK[:,1]}
avg_income_pandas = pd.DataFrame(data,columns=columns, index=index)


#Skrifum út í csv skrá og opnum í excel til þess að plotta niðurstöður úr töflu
avg_income_pandas.to_csv('avg_year.csv',encoding='utf-8')


