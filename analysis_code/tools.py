import glob
import numpy as np
import pandas as pd

def mun2ref(m):
    'convert munsell value to reflectance'
    def finv(y):
        y = np.array(y)
        x = np.empty(y.shape)
        i = y > ((841/108)*(24/116) ** 3) + (16/116)
        x[i] = y[i] ** 3
        x[~i] = (y[~i] - (16/116)) / (841/108)
        return x
    return finv((10 * m + 16) / 116)

def read_experiment(filt):
    'read text data files and return data frame for one experiment'
    flist = sorted(glob.glob(filt))
    dflist = [pd.read_csv(f, header=None, comment='#', skip_blank_lines=True)
                  for f in flist]
    for i, df in enumerate(dflist):
        df.insert(0, 'subject', i+1)
    df = pd.concat(dflist)
    return df

def load_trials(response1reflectance=True):
    'load and preprocess data from both experiments'
    df1 = read_experiment('data/expt1/*.txt')
    df1.insert(0, 'expt', 1)
    df2 = read_experiment('data/expt2/*.txt')
    df2.insert(0, 'expt', 2)
    df = pd.concat([df1, df2])
    df.columns = ['expt','subject','phase','trial','condition','fg_textype','fg_testlum',
                  'bg_textype','bg_motion','response1','rt1','response2','rt2']
    condition_names = ['baseline', 'bg-solid', 'bg-none', 'eroded', 'solo', 'motion', 'monoc',
                       'near','eroded-uniform', 'solo-motion', 'single-screen']
    df['condition'] = [condition_names[k-1] for k in df['condition'].values]  # replace condition numbers with condition names
    if response1reflectance:
        df['response1'] = mun2ref(df['response1'])  # convert munsell values to reflectance
    df.reset_index(inplace=True, drop=True)
    return df
