# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:30:34 2017

@author: Ruthberg

PREPROCESSING OF DATA USED TO ANALYZE A TANN MODEL (Technical Analysis Neural Network Model)

"""

#Import relevant packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Settings for calculations
filename = "GBPUSD_1_20171221"
normalize = True
#clen = 100 #length of calculation
mult = 1 #multiplier when calculating profit (seen as position)
tcost = 0.002 #transaction cost / spread in percent
point = 0.00001 #point value
leverage = 200 #depends on setting
trail = 200*point*mult #in currency units (trail specified in points)

#load data
dataframe = pd.read_csv(filename + ".csv", header = 0)
dlength = int(dataframe.size/len(dataframe))
dataset = dataframe.values
X=dataset[:, 4:dlength].astype(float)
Y=dataset[:,0].astype(float)
#Y.flags.writeable=True
bvec = Y.copy() #profit vector for buying
svec = Y.copy() #profit vector for selling

#ENCODING
#transform Y values to encoded BUY/HOLD/SELL in 1/0/-1
#Choice depends on which of the two gets stopped out at best profit
#assume this means the other direction implies a loss instead
high = X[:,1]*mult
low = X[:,2]*mult
close =X[:,3]*mult
hhigh = 0
llow = 0
hdiff = 0
ldiff = 0
bprof = 0
lprof = 0


it = np.nditer([Y,high,low,close,bvec,svec], op_flags=['readwrite'], flags=['f_index'])

for i,x,y,z,k,l in it:
    idx = it.index
    if idx == len(Y)-1: 
        i[...] = 0.5
        k[...] = 0
        l[...] = 0
        continue
    hhigh = x
    llow = y
    hdiff = hhigh - z #assume we trade on closes but that the
    ldiff = llow - z #trailing stops are calculated from new highs/lows
    newit = np.nditer([high[idx+1:],low[idx+1:],close[idx+1:]], op_flags=['readwrite'], flags=['f_index'])
    for q,w,e in newit:
        newidx = newit.index
        if newidx == len(Y)-1: 
            continue
        if q > hhigh:
            hhigh = q
        elif w < llow:
            llow = w
        hdiff = hhigh - e #assumption that we do not know enough whether the low will precede the high 
        ldiff = llow - e #hence to adjust for the otherwise perfect relationship, use hhigh-low
        if hdiff>= trail or ldiff <= -trail:
            bprof = (e-z)*leverage #if the new close stops us out, calculate profit
            lprof = -1*bprof #and break loop
            #print(svec[i], bvec[i], hdiff, ldiff, trail, close[i], close[i+j], close[i]-close[i+j], close[i+j]-close[i])
            break
    k[...] = bprof
    l[...] = lprof
   
    if l < k and k > z*tcost:
        i[...] = 1
    elif l > k and l > z*tcost:
        i[...] = 0
    else:
        i[...] = 0.5
    

profit = np.maximum.reduce([bvec,svec])
dat2 = {'Y': Y, 'Profit': profit}
df2 = pd.DataFrame(data=dat2)

if normalize:
    v = X[:,4]
    i1 = X[:,5]
    i2 = X[:,6]
    i3 = X[:,7]
    i4 = X[:,8]
    
    nmin = np.array([np.amin(v),np.amin(i1),np.amin(i2),np.amin(i3),np.amin(i4)])
    nmax = np.array([np.amax(v),np.amax(i1),np.amax(i2),np.amax(i3),np.amax(i4)])
    
    np.savetxt("TANN_Normalizations_Min" + ".csv", nmin, delimiter=",")
    np.savetxt("TANN_Normalizations_Max" + ".csv", nmax, delimiter=",")
    
    v = (v-np.amin(v))/(np.amax(v)) 
    i1 = (i1-np.amin(i1))/(np.amax(i1)) 
    i2 = (i2-np.amin(i2))/(np.amax(i2)) 
    i3 = (i3-np.amin(i3))/(np.amax(i3)) 
    i4 = (i4-np.amin(i4))/(np.amax(i4)) 
    


dat1 = {'Vol': v, 'RSI': i1, 'CCI': i2, 'ADX': i3, 'ATR': i4}

df1 = pd.DataFrame(data=dat1)    
new_dataframe = pd.concat([df1,df2],axis=1)
new_dataframe.to_csv(filename + "_Y.csv", index=False)

x=range(len(dataframe))
print("FINISHED! Results using trail at " + str(trail) + " currency units, where 1 point movement is " + str(point*mult) + " unit yields the below graph. Data stored with the filename " + filename + "_Y.csv" )
plt.plot(x,close+Y*trail,'--',x,close,'-')



"""
OLD CODE USING ARRAYS
for i in range(clen):
    hhigh = high[i]
    llow = low[i]
    hdiff = hhigh - close[i] #assume we trade on closes but that the
    ldiff = llow - close[i] #trailing stops are calculated from new highs/lows
    for j in range(clen-i):
        if j == 0: 
            continue
        if high[i+j] > hhigh:
            hhigh = high[i+j]
        elif low[i+j] < llow:
            llow = low[i+j]
        hdiff = hhigh - close[i+j] #assumption that we do not know enough whether the low will precede the high 
        ldiff = llow - close[i+j] #hence to adjust for the otherwise perfect relationship, use hhigh-low
        if hdiff>= trail or ldiff <= -trail:
            bprof = (close[i+j]-close[i])*leverage #if the new close stops us out, calculate profit
            lprof = -1*bprof #and break loop
            #print(svec[i], bvec[i], hdiff, ldiff, trail, close[i], close[i+j], close[i]-close[i+j], close[i+j]-close[i])
            break
    bvec[i] += bprof
    svec[i] += lprof
    if svec[i] < bvec[i]: # and bvec[i] > close[i]*tcost:
        Y[i] = 1
    elif svec[i] > bvec[i]: # and svec[i] > close[i]*tcost:
        Y[i] = -1
    else:
        Y[i] = 0
    print(Y[i],bvec[i], svec[i], bprof, lprof, hdiff, ldiff, hhigh, llow)
   """ 
        