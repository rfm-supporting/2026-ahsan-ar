import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import munsell

pool = True
reflectance = True

if pool:
    df = [ pd.read_csv(f, header=None, comment='#', skip_blank_lines=True) for f in glob.glob('data/*.txt')]
    df = pd.concat(df)
else:
    fname = 'matchar_subject10.txt'
    df = pd.read_csv(os.path.join('data',fname), header=None, comment='#', skip_blank_lines=True)

df.columns = ['phase','trial','condition','fg_textype','fg_testlum','bg_textype','bg_motion','response1','rt1','response2','rt2']
df['condition'] -= 1

if reflectance:
    df['response1'] = munsell.mun2ref(df['response1'])
    df['response2'] = munsell.mun2ref(df['response2'])

conditions = ['baseline', 'bg-solid', 'bg-none', 'eroded', 'solo', 'motion', 'monoc', 'near']

def plotone(df):
    dfg = df.groupby('fg_testlum')['response1'].mean()
    # plt.plot(df['fg_testlum'], df['response1'], 'o')
    label = conditions[df.reset_index()['condition'][0]]
    plt.plot(dfg.index, dfg, 'o-', label=label)
    return dfg.iloc[-1]

def plotc(cnamelist):
    ymaxlist = []
    for cname in cnamelist:
        cnum = conditions.index(cname)
        df2 = df[df['condition'] == cnum]
        ymax = plotone(df2)
        ymaxlist.append(ymax)

    ymax = np.array(ymaxlist).mean()
    ymaxref = ymax if reflectance else munsell.mun2ref(ymax)
    maxlum = df['fg_testlum'].max()
    xx = np.linspace(0,1.2*maxlum,100)
    yy = ymaxref * xx / maxlum if reflectance else munsell.ref2mun(ymaxref * xx/maxlum)
    plt.plot(xx, yy, 'k-', zorder=0, label='veridical')
    # *** the veridical line should be the same in all plots, at least for a given subject

    plt.xlim(0, 55)
    plt.xlabel('test patch luminance (cd/m$^2$)')
    if reflectance:
        plt.ylim(0, 0.75)
        plt.ylabel('mean reflectance rating')
    else:
        plt.ylim(3, 9)
        plt.ylabel('mean munsell rating')
    plt.legend(loc='lower right', frameon=False)
    plt.show()

plotc(['baseline', 'bg-solid', 'bg-none'])
plotc(['baseline', 'eroded', 'solo'])
plotc(['baseline', 'motion', 'monoc', 'near'])
