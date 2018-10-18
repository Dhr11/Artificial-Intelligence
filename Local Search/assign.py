#!/usr/bin/env python3
# Creators : Dhruuv Agarwal
#Problem of reducing time consumption on project team assignements
"""
As this problem consisted of possibly a unfeasibly huge state space if we went by traditional bfs or A*, 
 we looked to avoid generting all states. Thus we moved to Local Search and looked at the alternatives, 
 finally presenting the two approaches we took:       Greedy Beam and Monte carlo with some modifications


"""  
    

import sys
import random
from math import ceil,exp, floor
import numpy as np

## Making structure required from the input. The structure is dictionary with value
## as list of lists for each argument for an id/student
def Getinputfromfile(filepath):
    f =open(filepath, 'r', encoding = 'utf8')
    entries = [[x for x in line.split()] for line in f]
    d = {entry[0]:[int(entry[1]),[x for x in entry[2].split(',') if x!='_'],[x for x in entry[3].split(',')if x!='_']] for entry in entries}
    f.close()
    return d

##Eval group used to evaluate time consumed by a group
## Used by both approaches                
def EvalGroup(k, m, n, group, d):
    h = k
    for id1 in group:
        for id2 in group :
            if id1!=id2:
                if id2 in d[id1][2]:    
                    h+=m
        if d[id1][0]!=len(group) and d[id1][0]!=0:   h+=1
            
        for x in d[id1][1]:
             if x not in group:
                 h+=n 
                            
    return h
"""                                                                                             
Second and MAIN APPROACH
Monte Carlo with some Greediness involved in generating and choosing successor

Working really well and tested on 50, 100 sized dataset too. Might take some time as many iterations
 but still runs in less than a minute in our testing.
 Even if time is more in huge dataset, it will never get stuck and hence the patience will be rewarded 
 as value is lesser than normal Monte Carlo and Beam search

As the problem was optimization problem, hence local search was suitable. Among the others, Monte carlo looked 
promising as it didnt need to generate the whole successor set and look for the best among it.
Goal is just to minimize the function., and the state space initially is just the groups of size 2/3 combinations. That is 
how we get our initial state. After that the code sees if these groups can be rearranged, thus depending on the values
k,m,n we can have whole state space with combinations of groups of size 1,2,3


NOTE: This is the main algorithm used and is testing well compared to some of the peers we discussed with  
"""
def GreedyMonteCarlo(k, m, n, d):
    min = 0
    harr = []    
    board = []
    
    # As monte carlo might get stuc in local minima normally, so we run it for 15 times
    # just to have some decent init state and traversal depth for each
    for times in range(0,15):
        init_state = []
        IDleft = dict(d)
        # The intial state of monte carlo also isnt fully random
        # group size of 2/3 favors groups of more sizes and hence again relies on k>m & n
        while(len(IDleft.keys())>2):
            group_temp = random.sample(IDleft.keys(),random.randint(2,3))
            init_state.append(group_temp)
            [IDleft.pop(i,None) for i in group_temp]            
        if(len(IDleft)==1):
            [init_state.append([x]) for x in IDleft.keys()]
        if(len(IDleft)==2):
           init_state.append(random.sample(IDleft.keys(),2))     
        
        # For the same state we do 3000 iterations.
        cur_state = init_state
        for i in range(2000):
            ## Every iteration, takes two groups from state and tries to see if better group division exists
            grp1,grp2 = random.sample(cur_state,2)
            total = grp1+grp2
            hprev = EvalGroup(k,m,n,grp1,d)+EvalGroup(k,m,n,grp2,d)

            ## instead of generating the whole successor space or chossing randomly,
            ## the size of new group is determined by logic, like k>m,n and if not possible then look for other sizes
            ## and 2 preferred over 3 when same number of groups, as less chances of conflicts              
            if len(total)== 2:  sizearr = [[2]]
            elif len(total)== 3:  sizearr = [[3],[1,2]]
            elif len(total)== 4:  sizearr = [[2,2],[3,1]]
            elif len(total)==5:   sizearr = [[3,2],[2,2,1],[3,1,1]]
            elif len(total)==6:   sizearr = [[3,3],[2,2,2],[3,2,1],[2,2,1,1],[3,1,1,1]]            
            if(k<m):    sizearr.reverse()
            found = 0            
            for entry in sizearr: 
                for j in range(0,15):
                    tmptotal = list(total)
                    grpset = []
                    newh = 0
                    for size in entry:
                        newgrp = random.sample(tmptotal,size)
                        [tmptotal.remove(x) for x in newgrp]
                        newh += EvalGroup(k,m,n,newgrp,d)
                        grpset.append(newgrp)
              ## if the the new groups cost is less than selected two groups then switch the groups in the state      
                    if newh < hprev and newh!=0:
                        found = 1
                        cur_state.remove(grp1)
                        cur_state.remove(grp2)
                        [cur_state.append(x) for x in grpset]
                        break
                if(found==1):   break

        hfinal = 0
        for x in cur_state:
            hfinal += EvalGroup(k,m,n,x,d)                
        if min>hfinal or len(harr)==0:  
            min = hfinal
            board = cur_state
        harr.append(hfinal)
    
    p = np.min(harr)
    [print(' '.join(i)) for i in board]    
    print(p)
################################################################################################
"""First approach:            WORKING BUT VALUES NOT OPTIMIZED COMPARED TO THE SECOND APPROACH
#Greedy Beam approach
    
 This function is used to generate a group randomly. However we limit the randomness by constraints and assumptions
 Based on these assumptions we pass a limit on the time/cost and try to get our desired group if possible
"""
def GetSuccset(k,m,n,IDleft,size,limit):
    group = []
    for i in range(20):
        if size<=len(IDleft.keys()): group = random.sample(IDleft.keys(),size)
        if EvalGroup(k, m, n, group, IDleft)<=limit:  
            break
    return group   
                    
def CustomGreedyBeam(k, m, n, d):
    harr = []
    bestgroup =[]
    for i in range(6000):
        IDleft = dict(d)
        hinit = 0
        #print("Iteration ",i,"length ",len(IDleft.keys()))
        groups = []
        while IDleft.keys():
            succ = 0
            values = []
            ## logic on the limit of cost of each group, used to select the nexxt group
            if m>n: ratio_mn= floor(m/n)
            else :  ratio_mn= floor(n/m)
            if m>n: values1 = [ k+ i*n for i in range(0,ratio_mn)]    
            else :  values1 = [ k+ i*m for i in range(0,ratio_mn)]
            [ values.append(k1) for k1 in values1]
            values.sort()
            
            group = []
            for size in [3,2]:          # frist checks if size 3, within limit we get a group
                for limit in values:
                    group = GetSuccset(k,m,n,IDleft,size,limit)
                    if len(group)!=0:
                        succ = 1
                        break
                if succ==1:    break       
            if succ==0 and len(IDleft.keys())>1:    
                 group = random.sample(IDleft.keys(),2)
                 succ=1
            elif succ==0 and len(IDleft.keys())==1:  group = random.sample(IDleft.keys(),1)     
            groups.append(group)
            hinit += EvalGroup(k, m, n, group, IDleft)
            [IDleft.pop(i,None) for i in group]
        if not bestgroup or hinit<numpy.min(harr):
            bestgroup = groups
        harr.append(hinit)
    print(harr)
    print(numpy.min(harr))
    print(bestgroup)    

############################################################################################################
def solve():
    pass

d = Getinputfromfile(sys.argv[1])
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
GreedyMonteCarlo(k,m,n,d)