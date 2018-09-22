# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:30:34 2017

@author: Ruthberg

PREPROCESSING OF DATA USED TO ANALYZE A TANN MODEL (Technical Analysis Neural Network Model)

Use: choose how to process data/classify for subsequent use in a NN model. Input is a csv
with candle data (OHLC) along with TA/indicators used for input to the model. Output should
be the same data, normalized if necessary, along with a classifier for Buy/Sell. Script
should be flexible in the sense to choose target evaluation model, such as trailing stops
or simple stop loss with profit eval.

-preprocessing transforms Y values to encoded BUY/SELL as 1 or 0
-choice depends on which of the two does not get stopped out first
-trailing profit from entry point is used to determine which gets stopped out

"""

#Import relevant packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#File management
filename = "BTCUSD_1_20180101"
inpath = "data/"
outpath = "output/"
ftype = ".csv"

#Processing settings
normalize = True
normType = 3 #1 = (X - min(X))/max(X), 2 = X/mean(X), 3 = X-mean(X)
cleanOutput = True #set to True if output is to be cleaned from uncertain values = 0.5
#Stop strategy:
stopStrat = 1
 # 1 = FULL trail. Keep holding both b/s positions until trails stops. 2=SIMPLE trail wins. Stop when first gets out, opposite wins. 
 # 3 = FASTEST to profit wins. Without stopping out on SL. ..
mult = 1 #multiplier when calculating profit (seen as position)
tcost = 0.002 #transaction cost / spread in percent
#point = 0.00001 #point value
point = 0.01 #point value BTC
leverage = 200 #depends on setting
trailnum = 500 #trailing stop in points
trail = trailnum*point*mult #in currency units (trail specified in points)
maxTimePosition = 500 #max number of candles/time units a position can be held
startCol = 4 #column at which data starts
indStartCol = 8 #start column for indicator data / other predictors

#Load input data as a pd dataframe
dataframe = pd.read_csv(inpath + filename + ftype, header = 0)
dlength = int(dataframe.size/len(dataframe)) #number of cols in DF
dflen = len(dataframe) #number of rows in DF
dataset = dataframe.values
X=dataset[:, startCol:dlength].astype(float) #input dataset for processing
Y=dataset[:,0].astype(float)

#Define necessary vectors for processing
bvec = Y.copy() #BUY profit vector
svec = Y.copy() #SELL profit vector
cvec = Y.copy() #position time vector
opn = X[:,0]*mult
high = X[:,1]*mult
low = X[:,2]*mult
close =X[:,3]*mult

bprof = 0 #buy profit in curr it
sprof = 0 #sell profit in curr it
hhigh = 0 #highest high
llow = 0 #lowest low
hdiff = 0 #highest diff
ldiff = 0 #lowest diff
btrail = 0 #buy stop level
strail = 0 #sell stop level
bstopped = False
sstopped = False
clen = len(close) #length of series

#Iterate using np.nditer on df = [Y,high,low,close,bvec,svec] = i,x,y,z,k,l
it = np.nditer([Y,high,low,close,bvec,svec,cvec], op_flags=['readwrite'], flags=['f_index'])

for i,x,y,z,k,l,m in it:
    idx = it.index
    if idx >= clen-1: 
        i[...] = 0.5
        k[...] = 0
        l[...] = 0
        continue
    hhigh = x #current high in iteration
    llow = y #current low
    btrail = z - trail #stop levels. Assume we entered on the close and thus new trails directly from that price
    strail = z + trail 
    bstopped = False
    sstopped = False
    count = 0
    
    #Create new loop/iter to find stopout point. Stop when ... ? 1) First is stopped, 2) never (both might be stopped)
    newit = np.nditer([high[idx+1:],low[idx+1:],close[idx+1:]], op_flags=['readwrite'], flags=['f_index'])
    for q,w,e in newit:
        newidx = newit.index
        count = newidx
        if newidx >= clen-idx-1: 
            continue
        
        if stopStrat == 1 or stopStrat == 2:
            #Check if new highs/lows and if stopped out (assumes stops come before updating trail)
            if q > strail or w < btrail:
                if w < btrail and not bstopped:
                    bstopped = True
                    bprof = w - z #if the new low stops out the buy, calculate profit
                if q > strail and not sstopped:
                    sstopped = True
                    sprof = z - q 
                if stopStrat == 2 or (bstopped and sstopped):
                    break
            #Chek if new highs/lows and move trailing stops
            if q > hhigh:
                hhigh = q #new high
                btrail = hhigh - trail #buy trail moved up
            elif w < llow:
                llow = w #new low
                strail = llow + trail #sell trail moved down   
        if stopStrat == 3:
            bprof = e - z
            sprof = z - e
            if bprof > trail or sprof > trail:
                break
    
    #store profits
    k[...] = bprof
    l[...] = sprof
    m[...] = count
    
    #check best strategy
    if l < k and k > 0: #if buy is best and profitable
        i[...] = 1
    elif l > k and l > 0: #if sell is best and profitable
        i[...] = 0
    else: #otherwise discard
        i[...] = 0.5
    

#Prepare data output. df1 is original (normalized) indicator data
dat_list = list(dataframe)
dat1 = {}
nmin = np.array([])
nmax = np.array([])
nmean = np.array([])
currmin = 0
currmax = 0
currmean = 0
#df2 is classification and profit data
profit = np.maximum.reduce([bvec,svec])
dat2 = {'Y': Y, 'Profit': profit, 'Time' : cvec}
df2 = pd.DataFrame(data=dat2)
    
#Loop to prepare output dataset and normalize data
for i in range(dlength):
    if i < indStartCol:
        continue
    if normalize:
        currmin = np.amin(dataset[:, i].astype(float))
        currmax = np.amax(dataset[:, i].astype(float))
        currmean = np.mean(dataset[:, i].astype(float))
        nmin = np.append(nmin,currmin)
        nmax = np.append(nmax,currmax)
        nmean = np.append(nmean,currmean)
        if normType == 1:
            if currmax !=0:
                dat1[dat_list[i]] = (dataset[:, i].astype(float) - currmin)/currmax
            else:
                dat1[dat_list[i]] = 0
        elif normType == 2:
            dat1[dat_list[i]] = dataset[:, i].astype(float)/currmean
        elif normType == 3:
            dat1[dat_list[i]] = dataset[:, i].astype(float)-currmean
        else:
            dat1[dat_list[i]] = 0*dataset[:, i].astype(float)
    else:
        dat1[dat_list[i]] = dataset[:, i].astype(float)

#Save normalisations coefficients
if normalize:
    np.savetxt(outpath + "TANN_Normalizations_Min" + ".csv", nmin, delimiter=",")
    np.savetxt(outpath + "TANN_Normalizations_Max" + ".csv", nmax, delimiter=",")
    np.savetxt(outpath + "TANN_Normalizations_Mean" + ".csv", nmean, delimiter=",")

#Save output
df1 = pd.DataFrame(data=dat1)    
new_dataframe = pd.concat([df1,df2],axis=1)
new_dataframe = new_dataframe.iloc[:, ::-1]

if cleanOutput:
    new_dataframe = new_dataframe[new_dataframe['Y']!=0.5]

new_dataframe.to_csv(outpath + filename + "_Y.csv", index=False)

x=range(len(dataframe))
print("FINISHED! Results using trail at " + str(trail) + " currency units, where 1 point movement is " + str(point*mult) + " unit yields the below graph. Data stored with the filename " + filename + "_Y.csv" )
plt.plot(x,profit,'--')