# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:38:24 2020

@author: disha
"""

import matplotlib.pyplot as plt
import numpy as np 
import scipy.spatial
from PyAstronomy import pyasl
import pandas as pd
import seaborn as sns

### input parameters

q=4 ## q = (0,1,2,3,4) -> (left, right, bottom, top, center, peak (5))

image_position = [[[4, 8],[67, 24],[64, 27],[7, 5],[35, 15],[63, 24]], 
                  [[79, 10],[116, 23],[107, 28],[90, 3],[98, 15],[112, 24]],
                  [[40, 12],[117, 22],[67, 29],[62, 2],[76, 14],[113, 19]], 
                  [[3, 11],[87, 27],[84, 30],[21, 2],[45, 15],[84, 26]],
                  [[78, 16],[108, 16],[92, 24],[92, 9],[96, 14],[105, 13]]]

image_marker = ['left', 'right', 'bottom', 'top', 'cent']
image_label = ['Leftmost', 'Rightmost', 'Bottommost', 'Topmost', 'Centroid']

min_Xpixel = 0
max_Xpixel = 119 #not 120, because in Python 0 is included, so the length automatically becomes 120
min_Ypixel = 0
max_Ypixel = 60 #not 61, because in Python 0 is included, so the length automatically becomes 61

min_Xangle = 0
max_Xangle = 357
min_Yangle = -90
max_Yangle = 90

E_az = []
E_el = []
E_angular = []

################################################################################
    
def makeData(filename):      
    index = []
    point_az = []
    point_el = []
    sound_mode = []
    image_number = []
    image_pos = []
    x_offset = []
    user_id = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            columns = line.split(',')
            index =  int(columns[0])
            if index==0:
                if user_id == []:               
                    user_id.append(str(columns[1][1:5]))
                else:
                    if str(columns[1][1:5])!=user_id[-1]:
                        user_id.append(str(columns[1][1:5])) 
            if index in range(1,7):
                image_number.append(str(columns[1].strip(' " ')))
                sound_mode.append(str(columns[2].strip(' ')))
                image_pos.append(str(columns[3]).strip(' '))
                x_offset.append(float(columns[4]))
                point_az.append(float(columns[5]))
                point_el.append(float(columns[6].strip('"')))
          
    new_point_az = np.zeros(len(x_offset))
    new_point_el = np.zeros(len(x_offset))
    
    # mapping of user responses onto the image     
    for i in range(0,len(x_offset)):            
        new_point_az[i] = (point_az[i])/3 - (x_offset[i])
        if new_point_az[i] < 0:
            new_point_az[i] = (max_Xpixel) + new_point_az[i]
        new_point_el[i] = (point_el[i])/3 + max_Ypixel/2
     
    # some kind of D4 offset of 90 degrees (30 pixel units) along the azimuthal axis
    for i in range(0,len(x_offset)):            
        new_point_az[i] = new_point_az[i] - 30
        if new_point_az[i] < 0:
            new_point_az[i] = (max_Xpixel) + new_point_az[i]    
            
    data_d=[] #Euclidean miss-distance (in pixels)
    data_d_az_angle = [] #Horizontal miss-distance 
    data_d_el_angle = [] #Vertical miss-distance 
    data_angular_miss_distance = [] #Angular miss-distance (in angle)
    
    N = len(user_id) ## number of users
    print 'yoooo' + str(N)
    
    # Running a loop for all 5 images
    for r in range(0,5):
        az_amp_1=np.zeros(N)
        el_amp_1=np.zeros(N)
        j = 0
        A = [] #to store new locations in pixel units
        for i in range(0,len(x_offset)):
               if sound_mode[i]=='both' and image_number[i]==str(r+1) and image_pos[i]==image_marker[q]:
                    az_amp_1[j] = new_point_az[i]
                    el_amp_1[j] = new_point_el[i]
                    A.append((az_amp_1[j], el_amp_1[j]))  
                    j = j+1
                    
        # B stores the position of the centroid in pixel units          
        B = (image_position[r][q][0], -image_position[r][q][1]+max_Ypixel)   
        
        # d stores the euclidean distance of each point from the centroid  
        d_az = []
        d_el = []
        d = []
        for i in range(0,N):
                        d_az.append(scipy.spatial.distance.euclidean(A[i][0], B[0]))
                        d_el.append(scipy.spatial.distance.euclidean(A[i][1], B[1]))
                        d.append(scipy.spatial.distance.euclidean(A[i], B))
        
        phi_1 = []
        theta_1 = []
        # convert into degrees   
        for i in range(0,N):
            phi_1.append(A[i][0]*3)
            theta_1.append((A[i][1]-max_Ypixel/2)*3)
        
        # convert into degrees    
        phi_2, theta_2 = B[0]*3, (B[1]-max_Ypixel/2)*3
        
        d_az_angle = [] # angular separation along azimuth
        d_el_angle = [] # angular separation along elevation
        for i in range(0,N):
                if scipy.spatial.distance.euclidean(phi_1[i], phi_2)>180:
                    d_az_angle.append(360 - scipy.spatial.distance.euclidean(phi_1[i], phi_2))
                    print (360 - scipy.spatial.distance.euclidean(phi_1[i], phi_2))
                else:
                    d_az_angle.append(scipy.spatial.distance.euclidean(phi_1[i], phi_2))
                d_el_angle.append(scipy.spatial.distance.euclidean(theta_1[i], theta_2))
                    
        angular_miss_distance = []
        
        # https://pyastronomy.readthedocs.io/en/latest/pyaslDoc/aslDoc/angularDistance.html
        for i in range(0,N):
            angular_miss_distance.append(pyasl.getAngDist(phi_1[i], theta_1[i], phi_2, theta_2))
        
        # verifying it with the formula
        E=[]
        for i in range(0,N):
            E.append(np.rad2deg(np.arccos(np.sin(np.deg2rad(theta_1[i]))*np.sin(np.deg2rad(theta_2)) + np.cos(np.deg2rad(theta_1[i]))*np.cos(np.deg2rad(theta_2))*np.cos(np.deg2rad(phi_1[i])-np.deg2rad(phi_2)))))    
            #https://www.hs.uni-hamburg.de/DE/Ins/Per/Czesla/PyA/PyA/pyaslDoc/aslDoc/angularDistance.html

        data_d.append(d)
        data_d_az_angle.append(d_az_angle)
        data_d_el_angle.append(d_el_angle)
        data_angular_miss_distance.append(angular_miss_distance)
    
    if q==0 or q==1:
        return data_d_az_angle, user_id
    elif q==2 or q==3:
        return data_d_el_angle, user_id
    elif q==4:
        return data_angular_miss_distance, user_id
    
###############################################################################            
      
for s in range (0,2):
    if s==0:
        file_scenario = 'data/user-data-stationary.csv'
    else:
        file_scenario = 'data/user-data-moving.csv'
    #### angular miss-distance from the centroid
    E_angular.append(makeData(file_scenario)[0])
    
user_id =  (makeData(file_scenario)[1]) 
    
################################################################################

data_stat = {'User_id' : user_id,
        'Bow' : E_angular[0][0],
        'Ring' : E_angular[0][1],
        'Amoeba' : E_angular[0][2],
        'Snake' : E_angular[0][3],
        'Gradient' : E_angular[0][4],
        'Scenario' : np.repeat('Stationary',22)
        }

data_mov = {'User_id' : user_id,
        'Bow' : E_angular[1][0],
        'Ring' : E_angular[1][1],
        'Amoeba' : E_angular[1][2],
        'Snake' : E_angular[1][3],
        'Gradient' : E_angular[1][4],
        'Scenario' : np.repeat('Moving',22)
        }

df_stat = pd.DataFrame(data_stat)
df_mov = pd.DataFrame(data_mov)

df = df_stat.append(df_mov)

value_variables = ['Bow',
                   'Ring',
                   'Amoeba',
                   'Snake',
                   'Gradient']

id_variables = ['Scenario','User_id']

variable_name = 'Shapes'

df_melt = df.melt(id_vars = id_variables,
                  value_vars = value_variables,
                  var_name = variable_name)
        
################################################################################

def groupedBoxplots(data,value_variables, id_variables, variable_name, my_palette, xtickLabels,figname,ylabel, xlabel, figure_title,y_min,y_max):
    plt.style.use('default')    
    fig = plt.figure(1, figsize=(9,6))
    ax = fig.add_subplot(111)    

    sns.boxplot(data = data,
                hue = id_variables[0], # Scenario in this case
                x = variable_name,
                y = 'value',
                order = xtickLabels,
                palette = my_palette,
                saturation = 0.95,
                boxprops=dict(linestyle='-', linewidth=0.6),
                flierprops=dict(marker='o', markerfacecolor='#ef6eb0', markersize=6,linestyle='none'),
                medianprops=dict(linestyle='-', linewidth=1.85, color='#D3D3D3'),
                whiskerprops=dict(linestyle='-', linewidth=1.3, color='#003f5c'),
                capprops=dict(linestyle='-', linewidth=1.3, color='#003f5c'),
                showfliers=True)
                          
    ax.set_ylabel(ylabel, fontsize = 16)
    ax.set_xlabel(xlabel, fontsize = 16)
    ax.set_title(figure_title, fontsize = 16)
    ax.set_ylim(y_min,y_max) 
    ax.set_xticklabels(xtickLabels, rotation='0')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()   
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.tick_params(axis='x', which='major', labelsize=14) 
    fig.savefig('figures/fig-'+ figname +'.eps', format='eps', dpi=1000, bbox_inches='tight')


################################################################################
### Source: https://stackoverflow.com/questions/44975337/side-by-side-boxplots-with-pandas?rq=1

figname = 'grouped-boxplots-scenarios-'

if q==0 or q==1:
    ylabel = 'Azimuthal Miss-distance (in degrees)'
    y_max = 185 
    figname = figname + 'az-q'
elif q==2 or q==3:
    ylabel = 'Elevation Miss-distance (in degrees)'
    y_max = 85
    figname = figname + 'el-q'
elif q==4:
    ylabel = 'Angular Miss-distance (in degrees)'
    y_max = 125
    figname = figname + 'q'
    
y_min = -5
xtickLabels = (value_variables)   
xlabel = ' '

figure_title = image_label[q]
figname = figname +str(q)

my_palette = {'Stationary' : '#58508d',
        'Moving' : '#ffa600'}

groupedBoxplots(df_melt,value_variables, id_variables,variable_name, my_palette, xtickLabels,figname, ylabel, xlabel, figure_title,y_min,y_max)
                     
plt.show()

################################################################################

#df_melt.to_csv(r'data\miss-distances-' + str(q) +'.csv', encoding = 'utf-8', mode = 'w')
