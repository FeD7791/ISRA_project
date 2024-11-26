import pandas as pd 
import numpy as np
import seaborn as sns
from tools import load_isra

final_df = load_isra(n_examples=100,data_path='./data')