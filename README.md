El algoritmo contiene las siguientes funciones ubicadas en el modulo tools.py </br>
- cfm_slicer(Dataframe): Toma el Dataframe obtenido a partir de la hoja de calculo y lo divide en tres Dataframe: C,F,M </br>
- all_s_isra(Dataframe): Toma el Dataframe obenico a partir de la hoja de calculo (por lo cual contiene los elementos C,F,M) y calcula S1,S2, . . . ,S22 (Se devuelve en un diccionario) </br>
- re_isra(dict): Calcula los valores F1,F2,F3,F4 a partir de un diccionario otorgado por la funcion anterior. Retorna un diccionario con todos estos valores.
- rg_isra(Dataframe): Toma un dataframe con C,F,M y calcula sum_jC_j , sum_jF_j , sum_jM_j y TOTAL = sum_jC_j+sum_jF_j+sum_jM_j . El valor de esto se entrega en un diccionario. </br>
- baremos_isra(dict,sexo,caso): Toma el diccionario entregado por la funcion anterior y utiliza los baremos para calcular los centiles asociados a cada uno de ellos. Los baremos requieren especificar el sexo y el caso. Entrega un diccionarios con los centiles correspondientes
Observacion 1: Requeriria incluir el sexo en la tabla </br>
- a_classification(centiles_dict): A partir del diccionario de centiles se da una clasificacion de [ A-minima, A-marcada, A-severa, A-extrema ]
