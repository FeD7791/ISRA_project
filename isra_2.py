import os
import pathlib

import attrs
import pandas as pd
import numpy as np







@attrs.define
class Paciente:
    _sexo = attrs.field()
    _poblacion = attrs.field()
    _cfm = attrs.field()
    _baremos = attrs.field()


    @property
    def sexo(self):
        return self._sexo
    @property
    def poblacion(self):
        return self._poblacion
    @property
    def cfm(self):
        """Input DataFrame"""
        return self._cfm
    @property
    def baremos(self):
        return self._baremos
    
    @baremos.setter
    def age(self, value):
        path_baremos = pathlib.Path(os.path.abspath(value) / f'Baremos/{self._poblacion}/{self._sexo}.xlsx')
        baremos = pd.read_excel(path_baremos)
        self._baremos = baremos
    


    

    def sistema_de_respuesta(self, sistema):

        c_names = [f'C{n}' for n in range(1,8)]
        f_names = [f'F{n}' for n in range(1,11)]
        m_names = [f'M{n}' for n in range(1,8)]

        if sistema=='cognitivo':
            return _sistemas_de_respuesta(df=self.cfm, names_= c_names)
        if sistema=='fisiologico':
            return _sistemas_de_respuesta(df=self.cfm, names_= f_names) / 2
        if sistema=='motor':
            return _sistemas_de_respuesta(df=self.cfm, names_= m_names)
        if sistema=='total':
            c = _sistemas_de_respuesta(df=self.cfm, names_= c_names)
            f = _sistemas_de_respuesta(df=self.cfm, names_= f_names) / 2
            m = _sistemas_de_respuesta(df=self.cfm, names_= m_names)
            return c + f + m
        
    def rasgos_especificos(self, f_n):
        return _rasgos_especificos(df=self.cfm, n=f_n)
    
    def class_ansiedad(self, baremos_path):
        rasgos_especificos = {
            'C' : self.sistema_de_respuesta(sistema='cognitivo'),
            'F' : self.sistema_de_respuesta(sistema='fisiologico'),
            'M' : self.sistema_de_respuesta(sistema='motor'),
            'TOTAL' : self.sistema_de_respuesta(sistema='total')
        }
        return baremos_interface(
            baremos_path=baremos_path,
            rg_dict=rasgos_especificos,
            sexo=self._sexo,
            caso=self._poblacion
            )



def read_table(path):
    """Reads an input excel table.
    Parameters
    ----------
        Path: input file path
    Returns
    -------
        df_full
            Full dataframe of c,f, and m values
        list
            List of c,f and m names
    """
    df = pd.read_excel(path)
    c_names = [f'C{n}' for n in range(1,8)]
    f_names = [f'F{n}' for n in range(1,11)]
    m_names = [f'M{n}' for n in range(1,8)]

    df_full = df[c_names + f_names + m_names]
    df_full.fillna(0, inplace=True)
    df_full.drop(df_full.index[-1], inplace=True)

    return df_full, [c_names, f_names, m_names]

def calculate_s_sum(df, index):
    return df.iloc[index].sum()


def _rasgos_especificos(df, n):

    f1_indexes = [1,4,8,10,11,13]
    f2_indexes = [7,15,18]
    f3_indexes = [12,14,17,19]
    f4_indexes = [5,21,22]

    indexes_ = [f1_indexes, f2_indexes, f3_indexes, f4_indexes]
    
    return _fx(df=df, indexes=indexes_[n])


def _fx(*, df, indexes):
    s_sum = [df.iloc[idx].sum() for idx in indexes]
    return np.sum(s_sum)


def _sistemas_de_respuesta(df, names_):
    """Caluclates the 'Sistemas de Respuesta'. The kind of systems is computed
    based on the names_ parameter.

    Parameters
    ----------
        df : DataFrame
            Input excel file in DataFrame form.
        names_ : list , any of: [c_names, f_names, m_names]
            Names of the dataframe to calculate the 'sistema de respuesta'.
            c_names : Cognitivo
            f_names : Fisiologico
            m_names : Motor
    Returns
    -------
        float
            Sum of the desired paramter.
    """
    return np.sum([df[name].sum() for name in names_])

# =============================================================================
# OLD
# =============================================================================

def baremos_interface(baremos_path, rg_dict, caso, sexo):
    cases = [
        ('clinico','varon'),
        ('clinico','mujer'),
        ('normal','varon'),
        ('normal','mujer')
        ]

    if (caso,sexo) not in cases:
        raise AttributeError(
            'Incorrect value of sexo/caso, valid attributes are: \
                clinico/normal - varon/mujer'
            
            ) 

    # path_baremos = f'./Baremos/{caso}/{sexo}.xlsx' #Requiere openpyxl
    baremos = pd.read_excel(baremos_path)

    centiles = _baremos_isra(baremos=baremos, rg_dict=rg_dict)
    return _a_classification(centiles_dict=centiles)

def _baremos_isra(baremos, rg_dict):
    """
   Calculates and returns centiles based on ISRA scores and reference tables.

   Parameters
   ----------
   rg_dict : dict
       A dictionary containing ISRA scores (C, F, M, TOTAL).
   sexo : str, {'varon','mujer'}
       The sex of the individual for whom centiles are being calculated.
   caso : str, {'clinico','normal'}
       The type of case for which centiles are being calculated.

   Returns
   -------
   dict
       A dictionary containing the calculated centiles for C, F, M, and TOTAL
       scores.

   Raises
   ------
   AttributeError
       If the provided sexo or caso values are not valid.
   """
    


    C = rg_dict['C']
    F = rg_dict['F']
    M = rg_dict['M']
    TOTAL = rg_dict['TOTAL']
    list_elements = [
        ('C',C,'cognitivo'),
        ('F',F,'fisiologico'),
        ('M',M,'motor'),
        ('TOTAL',TOTAL,'total')
        ]
    centiles = {}
    for j in list_elements:
        for i in np.arange(0,18):
            if j[1] <= baremos[j[2]][19]:
                centiles[j[0]] = baremos['centil'][19]
                break
            elif baremos[j[2]][i+1] <= j[1] and j[1] <= baremos[j[2]][i]:
                centiles[j[0]] = baremos['centil'][i]
                break
            elif j[1] > baremos[j[2]][0]:
                centiles[j[0]] = baremos['centil'][0]
                break
    return centiles


def _a_classification(centiles_dict):
    """
   Assigns A-level classifications based on provided centiles.

   Parameters
   ----------
   centiles_dict : dict
       A dictionary containing centiles for C, F, M, and TOTAL scores.

   Returns
   -------
   dict
       A dictionary containing the assigned A-level classifications for \
        C, F, M, and TOTAL scores.

   Raises
   ------
   ValueError
       If the provided centiles_dict does not contain the expected keys \
        (C, F, M, TOTAL).
   """
    limits = [20,75,95]
    a_levels = ['A-minima','A-marcada','A-severa','A-extrema']
    a_dict = {}
    for i in ['C','F','M','TOTAL']:
        if centiles_dict[i] <= limits[0]:
            a_dict[i] = a_levels[0]
        elif limits[0] < centiles_dict[i] <= limits[1]:
            a_dict[i] = a_levels[1]
        elif limits[1] < centiles_dict[i] <= limits[2]:
            a_dict[i] = a_levels[2]
        elif centiles_dict[i] > limits[2]:
            a_dict[i] = a_levels[3]
    return a_dict
