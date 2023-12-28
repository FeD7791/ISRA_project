import pandas as pd 
import numpy as np



def cfm_slicer(user_df):
    """
    Slices a DataFrame into three smaller DataFrames based on specific column ranges.

    Parameters
    ----------
    user_df : pandas.DataFrame
        The input DataFrame to be sliced.

    Returns
    -------
    dict
        A dictionary containing three DataFrames:
        - C_df: DataFrame containing columns 2 to 8 and rows 0 to 21 (inclusive).
        - F_df: DataFrame containing columns 10 to 19 and rows 0 to 21 (inclusive).
        - M_df: DataFrame containing columns 21 to 27 and rows 0 to 21 (inclusive).

    Raises
    ------
    ValueError
        If the input DataFrame does not have the expected dimensions or column names.
    """
    C_df = user_df.iloc[0:22,2:9]
    F_df = user_df.iloc[0:22,10:20]
    M_df = user_df.iloc[0:22,21:28]
    return {'C':C_df,'F':F_df,'M':M_df}


def all_s_isra(user_df):
    """Calculates S scores based on specific columns of a DataFrame.

   Parameters
   ----------
   user_df : pandas.DataFrame
       A DataFrame with at least 28 columns. Columns 2-8, 10-20, and 21-28
       are assumed to contain numerical values.

   Returns
   -------
   dict
       A dictionary with 21 keys (S1 to S21), each containing a numerical value
       calculated as the sum of values from specific columns of the input DataFrame.

   Raises
   ------
   ValueError
       If the input DataFrame does not have the required number of columns or
       if the specified columns do not contain numerical values.
   """
    S = {}

    for i in np.arange(0,21):
       S[f"S{i+1}"] = user_df.iloc[i,2:9].sum() + user_df.iloc[i,10:20].sum() + user_df.iloc[i,21:28].sum()

    return S

def re_isra(s_dict):
    """Calculates scores based on a dictionary of values.

   Parameters
   ----------
   s_dict : dict
       A dictionary with keys 'S1', 'S4', 'S5', 'S7', 'S8', 'S10', 'S11', 'S12',
       'S13', 'S14', 'S15', 'S17', 'S18', 'S19', 'S21', and 'S22', containing
       numerical values.

   Returns
   -------
   dict
       A dictionary containing four scores:
       - 'F1': The sum of values for keys 'S1', 'S4', 'S8', 'S10', 'S11', and 'S13'.
       - 'F2': The sum of values for keys 'S7', 'S15', and 'S18'.
       - 'F3': The sum of values for keys 'S12', 'S14', 'S17', and 'S19'.
       - 'F4': The sum of values for keys 'S5', 'S21', and 'S22'.

   Raises
   ------
   KeyError
       If any required keys are missing in the input dictionary.
   ValueError
       If any of the required values in the input dictionary are not numerical.
   """
    F_scores = {}
    F1 = s_dict['S1'] + s_dict['S4'] + s_dict['S8'] + s_dict['S10'] +s_dict['S11'] + s_dict['S13']
    F2 = s_dict['S7'] + s_dict['S15'] + s_dict['S18']
    F3 = s_dict['S12'] + s_dict['S14'] + s_dict['S17'] + s_dict['S19']
    F4 = s_dict['S5'] + s_dict['S21'] + s_dict['S22']
    F_scores['F1'] = F1
    F_scores['F2'] = F2
    F_scores['F3'] = F3
    F_scores['F4'] = F4
    return F_scores

def rg_isra(user_df):
    """
    Calculates and returns values related to ISRA scores from a DataFrame.

    Parameters
    ----------
    user_df : pandas.DataFrame
        A DataFrame containing ISRA data, with scores in specific columns.

    Returns
    -------
    dict
        A dictionary containing the following calculated scores:
        - C: Sum of scores from columns 2 to 8 in row 22 (index 21).
        - F: Sum of scores from columns 10 to 19 in row 22, divided by 2.
        - M: Sum of scores from columns 21 to 27 in row 22.
        - TOTAL: The sum of C, F, and M scores.

    Raises
    ------
    ValueError
        If the input DataFrame does not have the expected structure or data types.
    """
    C = user_df.iloc[22,2:9].sum()
    F = user_df.iloc[22,10:20].sum() / 2
    M = user_df.iloc[22,21:28].sum()
    TOTAL = C + F + M
    return {'C':C , 'F':F, 'M':M, 'TOTAL':TOTAL}
    
def baremos_isra(rg_dict,sexo,caso):
    """
   Calculates and returns centiles based on ISRA scores and reference tables.

   Parameters
   ----------
   rg_dict : dict
       A dictionary containing ISRA scores (C, F, M, TOTAL) as calculated by the rg_isra function.
   sexo : str, {'varon','mujer'}
       The sex of the individual for whom centiles are being calculated. Valid values are 'varon' or 'mujer'.
   caso : str, {'clinico','normal'}
       The type of case for which centiles are being calculated. Valid values are 'clinico' or 'normal'.

   Returns
   -------
   dict
       A dictionary containing the calculated centiles for C, F, M, and TOTAL scores.

   Raises
   ------
   AttributeError
       If the provided sexo or caso values are not valid.
   """
    
    cases = [('clinico','varon'),('clinico','mujer'),('normal','varon'),('normal','mujer')]

    if (caso,sexo) not in cases:
        raise AttributeError('Incorrect value of sexo/caso, valid attributes are: clinico/normal - varon/mujer') 

    path_baremos = f'../Baremos/{caso}/{sexo}.xlsx' #Requiere openpyxl
    baremos = pd.read_excel(path_baremos)

    C = rg_dict['C']
    F = rg_dict['F']
    M = rg_dict['M']
    TOTAL = rg_dict['TOTAL']
    list_elements = [('C',C,'cognitivo'),('F',F,'fisiologico'),('M',M,'motor'),('TOTAL',TOTAL,'total')]
    centiles = {}
    for j in list_elements:
        for i in np.arange(0,18):
            if j[1] <= baremos[j[2]][19]:
                centiles[j[0]] = baremos['centil'][19]
            elif baremos[j[2]][i+1] < j[1] and j[1] <= baremos[j[2]][i]:
                centiles[j[0]] = baremos['centil'][i]
            elif j[1] > baremos[j[2]][0]:
                centiles[j[0]] = baremos['centil'][0]
    return centiles  
     
def a_classification(centiles_dict):
    """
   Assigns A-level classifications based on provided centiles.

   Parameters
   ----------
   centiles_dict : dict
       A dictionary containing centiles for C, F, M, and TOTAL scores.

   Returns
   -------
   dict
       A dictionary containing the assigned A-level classifications for C, F, M, and TOTAL scores.

   Raises
   ------
   ValueError
       If the provided centiles_dict does not contain the expected keys (C, F, M, TOTAL).
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

