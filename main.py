import pandas as pd 
import numpy as np
from tools import rg_isra,baremos_isra,a_classification

elements = []
lista = ["%04d" % x for x in range(16)]
lista.remove('0000')

for e in lista:

    path = f'./database/ISRA_{e}.xlsx'
    
    data = pd.read_excel(path)
    names = list(data)[2:9] + list(data)[10:20] + list(data)[21:29]
    df = pd.concat([data.iloc[22,2:9],data.iloc[22,10:20]])
    pd.concat([df,data.iloc[22,21:29]])
    doct = zip(names,df)
    new_row = dict(doct)

    ##Pipeline find type
    cfm_scores = rg_isra(data)
    cfm_centiles = baremos_isra(cfm_scores,'mujer','normal')
    a_type = a_classification(cfm_centiles)

    new_row['A-type'] = a_type['TOTAL']
    # new_row['C-A-TYPE'] = a_type['C']
    # new_row['F-A-TYPE'] = a_type['F']
    # new_row['M-A-TYPE'] = a_type['M']
    # new_row['A-TYPE'] = a_type['TOTAL']
    elements.append(new_row)

final_df = pd.DataFrame(elements)
print(final_df.head())



 
