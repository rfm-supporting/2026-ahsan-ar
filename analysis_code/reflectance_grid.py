import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tools

df = tools.load_trials()

def make_grid(dfx, row_permute, ylabels, fname):
    dfg = pd.pivot_table(dfx, index='condition', columns='fg_testlum', values='response1', aggfunc='mean')
    dfg = dfg.iloc[row_permute]
    print(dfg)
    image = dfg.to_numpy() / 0.85
    plt.imshow(image, cmap='gray', vmin=0, vmax=1)
    plt.xticks(ticks=range(len(dfg.columns)), labels=dfg.columns)
    plt.xlabel('test luminance (cd/m$^2$)')
    plt.yticks(ticks=range(len(ylabels)), labels=ylabels)
    plt.savefig(fname)
    plt.show()

df1 = df[df['expt']==1]
make_grid(df1, row_permute=[0,1,2,7,3,4,6,5], 
    ylabels=['Baseline', 'No Background', 'Solid Background', 'Solo', 'Eroded', 'Monocular', 'Near', 'Moving-Background'],
    fname='grid_experiment1.tif')
    
df2 = df[df['expt']==2]
make_grid(df2, row_permute=[0,1,2,5,6,3,4], 
    ylabels=['Baseline', 'Eroded', 'Eroded-Uniform', 'Solo', 'Solo-Motion', 'Near', 'Single-Screen'],
    fname='grid_experiment2.tif')
