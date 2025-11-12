import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

datafiles = {'23605': 'data/CvT_db/1_Blood_subject74_series_23605_data.csv',
             '23630': 'data/CvT_db/2_breath_subject74_series_23630_data.csv',
             '23582':'data/CvT_db/subject74_series_23582_data.csv',
             '23583':'data/CvT_db/subject74_series_23583_data.csv',
             '23612': "data/CvT_db/subject74_series_23612_data.csv"}

for key, filepath in datafiles.items():
    data = pd.read_csv(filepath)

    x=data['time_original'].values
    y=data['conc_original'].values

    plt.figure(figsize=(10,6))
    plt.plot(x, y, 'o', color='b')

    plt.title(f'{key} Concentration vs Time')

    plt.xlabel('Time (original)')
    plt.ylabel('Concentration (original)')
    plt.grid(True)
    plt.savefig(f"data/image/{key}_concentration_vs_time.png")
    plt.show()

