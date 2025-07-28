import attrs
import pandas as pd
import numpy as np

@attrs.define
class Paciente:
    _sexo = attrs.field()
    _poblacion = attrs.field()
    _cfm = attrs.field()


    @property
    def sexo(self):
        return self._sexo
    @property
    def poblacion(self):
        return self._poblacion
    @property
    def cfm(self):
        return self._cfm
    

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
        
    def rasgos_especificos(self, f_n):
        return _rasgos_especificos(df=self.cfm, n=f_n)



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
