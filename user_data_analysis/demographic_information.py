# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 00:18:58 2020

@author: disha
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fileName = 'demographic_information_imageTest_2018.csv'

df = pd.read_csv(fileName)

dResults = {}

keys = ['Definite prior exposure to a spatial sound environment',
        'Prior experience with gesture based interfaces',
        'Right-handed',
        'Male',
        'Age (18-30)']

values = [df[df.columns[5]].value_counts(normalize=True)[0],
          df[df.columns[6]].value_counts(normalize=True)[0],
          df[df.columns[4]].value_counts(normalize=True)[0],
          df[df.columns[2]].value_counts(normalize=True)[0],
          0.818182]
#   check the following value and change the last value in values and the age range in keys accordingly
#   df[df.columns[1]].value_counts(bins=2, normalize=True)]

for i in range(len(keys)):
    dResults.__setitem__(keys[i], [values[i]])
    
### Source: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py   

def survey(results):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    print data[0]
#    category_colors = plt.get_cmap('inferno')(np.linspace(.15, 0.85, data.shape[1]))
    label_colors = [[0, 63./255., 92./255.,1.],
                    [88./255., 80./255., 141./255.,1.], 
                    [188./255., 80./255., 144./255.,1.],
                    [255./255., 99./255., 97./255.,1.],
                    [255./255., 166./255., 0.,1.]]
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    # get rid of the frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
#    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlim(0, 1)
    ax.set_axisbelow(True)
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off    
    
    widths = data[:,0]  
    ax.barh(labels, widths, left=0, height=0.45, 
            color=label_colors, alpha=0.9, edgecolor=label_colors, linewidth=3 )
    xcenters = widths + 0.1
    
#   r, g, b, _ = color
#   text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
    text_color = 'black'
    for y, (x, c, l) in enumerate(zip(xcenters, widths, labels)):
        if c != 0:
            ax.text(x-0.01, y, str(round(c,4)*100)+'%', ha='center', va='center',
                color=text_color, fontsize=14, fontstyle = 'normal', fontweight = 'semibold')
            ax.text(0, y+0.45, l, ha='left', va='center',
                color=text_color, fontsize=16, fontstyle = 'normal', fontweight = 'light')
#    ax.legend(ncol=len(category_names)-3, bbox_to_anchor=(0, 1),loc='lower left', fontsize=16)
    ax.grid(b=None, which='both', axis='both', linestyle='--')
    plt.tight_layout()
    return fig, ax

survey(dResults)
#plt.title('Particpants Demographics', fontsize=20 )
#plt.savefig('participants_demographics.png', format='png', dpi=500,bbox_inches = 'tight')
plt.show() 

    
