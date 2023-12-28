import pandas as pd 
import numpy as np
from tools import rg_isra,baremos_isra,a_classification,cfm_slicer


lista = ["%04d" % x for x in range(16)]
lista.remove('0000')



dataset = {}
C = []
F = []
M = []
target = []

for e in lista:
    path = f'../database/ISRA_{e}.xlsx'
    data = pd.read_excel(path)
    #Pipeline
    cfm_scores = rg_isra(data)
    cfm_centiles = baremos_isra(cfm_scores,'mujer','normal')
    a_type = a_classification(cfm_centiles)
    cfm_slices = cfm_slicer(data)

    

    C.append(cfm_slices['C'])
    F.append(cfm_slices['F'])
    M.append(cfm_slices['M'])
    target.append(a_type['TOTAL'])
    
######



dataset['C'] = C 
dataset['F'] = F 
dataset['M'] = M
dataset['target'] = target

dataset_df = pd.DataFrame(dataset)

print(list(dataset_df))
print(dataset_df['C'][0].shape, dataset_df['F'][0].shape, dataset_df['M'][0].shape)




