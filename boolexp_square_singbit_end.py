# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 23:06:58 2015

@author: aguevarr
"""

from sympy import SOPform, Or, And, Not, Xor
import numpy as np
import pandas as pd
import string
import copy as cp
import pickle
from timeit import default_timer as timer
import matplotlib.pyplot as plt
#do 20 bits

def dec2bin(num,wid):
    x=list(np.binary_repr(num,width=wid))
    return map(int,x)
    
#become an object?
def rmme(arr,glob):
    if arr in glob:
        glob.remove(arr)
        return 
    else:
        return 

def apme(arr,glob):
    if arr in glob:        
        return 
    else:
        glob.append(arr)
        return 

def plotit(ymin,ymax):
    global inindex,invalues
    inindex=[]
    invalues=[]
    for x in xrange(len(stimes.index)-1):
        if (stimes.index[x+1]-stimes.index[x] > 1):
            split=(stimes.values[x]/(stimes.index[x+1]-stimes.index[x]))
            inindex.append(stimes.index[x])
            invalues.append(stimes.values[x])
            for y in xrange(1,(stimes.index[x+1]-stimes.index[x])):
                inindex.append(stimes.index[x]+y)
                invalues.append(split)              
        else:
            inindex.append(stimes.index[x])
            invalues.append(stimes.values[x])
    plt.ylim(ymin,ymax)
    plt.plot(inindex,invalues)

def rolmean(win):
    scompl=pd.Series(invalues,index=inindex)
    plt.plot(inindex,pd.rolling_mean(scompl,win))
    
ans=1
noinpbits=13
numxx=11
probe=14
newlength=noinpbits*2
inpmax=(2**noinpbits)-1
ansbin=[dec2bin(ans,newlength)]
for x in xrange(2,inpmax):
    ans=x**2
    ansbin=np.append(ansbin,[dec2bin(ans,newlength)],axis=0)

dontcares=[dec2bin(0,noinpbits)]
for x in xrange(1,inpmax+1):
    dontcares.append(dec2bin(x,noinpbits))
minterms=[]
#generate list of vars

varnames=[]
#for newly inserted variables
for x in xrange(noinpbits-11):
    varnames.append('a'+str(x))
    
for x in xrange(11):
    varnames.append('x'+str(x))


    
vdict={}
stopit=0
no=1
y=0
doneit=0
numx=(2**noinpbits-2)-2**numxx
inputs=[]
for x in xrange(1,inpmax):
    inputs.append(dec2bin(x,noinpbits))

start = timer()    
for x in xrange(no):    
    for y in xrange(len(ansbin)):    
        #for optimization
        notrain= y<numx
        gtrain= y>numx 
        if (stopit==1):
            stopit=0
            print y-1
            print timer()-start
            #save here
#            output = open('funclistv2_b7.pkl', 'wb')
#            pickle.dump(funclist,output)
#            output.close()
#            output = open('mintermsv2_b7.pkl', 'wb')
#            pickle.dump(minterms,output)
#            output.close()
#            output = open('dontcaresv2_b7.pkl', 'wb')
#            pickle.dump(dontcares,output)
#            output.close()
#            stimes.to_csv('stimes_b7.csv')
#            start=timer()
            break
        for zz in xrange(newlength-probe+1,newlength-probe+2):
            if (gtrain):
                for kk in xrange(len(varnames)):
                    vdict[varnames[kk]]=inputs[y][kk] 
                val=funclist.subs(vdict)
            if (ansbin[y][zz]==1) and notrain:
                apme(inputs[y],minterms)
                rmme(inputs[y],dontcares)
                continue
            elif (ansbin[y][zz]==0) and notrain:
                rmme(inputs[y],dontcares)  
                continue
            elif y==numx and doneit==0:
                print 'already here'
                funclist=SOPform(varnames,minterms,dontcares) 
                doneit=1
            elif (val==True) and (ansbin[y][zz]==1) and gtrain and (y<(2**noinpbits-3)):
                apme(inputs[y],minterms)
                rmme(inputs[y],dontcares)
#                print val
                continue
            elif (val==False) and (ansbin[y][zz]==0) and gtrain and (y<(2**noinpbits-3)):
                rmme(inputs[y],dontcares)
#                print val
                continue
            elif (val==True) and (ansbin[y][zz]==1) and (y==(2**noinpbits-3)):
#                print val
                print 'learned'
                print timer()-start
                break
            elif (val==False) and (ansbin[y][zz]==0) and (y==(2**noinpbits-3)):
#                print val
                print 'learned'
                print timer()-start
                break
            else:
                stopit=1
                print '-->bit '+str(zz)+' y='+str(y)
#                if (ansbin[y][zz]==1):
#                   #minterm
#                   apme(inputs[y],minterms)
#                   rmme(inputs[y],dontcares)
#                   funclist=SOPform(varnames,minterms,dontcares) 
#                elif (ansbin[y][zz]==0):
#                   rmme(inputs[y],dontcares)
#                   funclist=SOPform(varnames,minterms,dontcares)      
                   






