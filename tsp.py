# -*- coding: utf-8 -*-
'''
    旅行者問題的演算法實做
'''
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#inf = sys.maxint # 代表不能直接走到的城鎮距離
inf = 50


cityNode = np.array( [ (2,3), (0,3), (0.5,3),( 4,1), (-2,-1), (1,5), (3,2), (0,-1) ] ) #各節點的位置
citys = range( len(cityNode) ) # 節點編號


'''
    計算節點之間的距離
'''
def euclidean_distance( a, b ):
    return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2  )

'''
    得到城鎮的子集合
    子集合的取法是設想所有元素都具有，在或不在
    因此有2^len(set) 種組合
'''
def findAllSubset():
    l = 2**len(cityNode)
    binDigit = len(citys) # 二進位下的位數
    subsetBin = [] # 子集合中元素的形式 以0:不存在,1:存在
    subsets = []
    for i in range(0, l):
        s = bin(i)
        s = s.split('0b')[1]
        s = s.zfill( binDigit  )
        subsetBin.append( s )

    for i in subsetBin: # 做出子集合
        oneSubset = [] 
        for j in xrange( len(i) ):
            if '1' == i[j]:
                oneSubset.append( citys[j] )
        subsets.append( oneSubset )

    return sorted(subsets, key=lambda e: ( len(e), e[0] ) if len(e) else 0 ) #將子集合以元素個數及節點編號排序
 
def tsp():
    subsets = findAllSubset() 
    n = len(citys)
    D = [] # 存放走訪節點的花費
    middle = [] # 存放經過的中途節點

    '''
        初始化
    '''
    for i in xrange(n):
        D.append( [] )
        middle.append( [] )
        for j in xrange( len(subsets) ):
            D[i].append( inf )
            middle[i].append( inf )

    for i in xrange(1, n):
        D[i][0] = euclidean_distance( cityNode[0], cityNode[i] ) 


    '''
        TSP algorithm 
    '''
    for k in xrange(0, n-1 ):
        A = [ j for j in subsets if k == len(j) and 0 not in j ] # 包含k個點的子集合們 且不包含起始點
        p = []
        for a in A:
            for i in xrange(0, n): #以節點i當成起點，看看走子集內其他點所需的花費 
                ap =[ x for x in a if x != i ] 
                m = inf 
                mp = -1 
                for j in xrange(0, n): #以子集中一點當中途點，看看從節點i出發，透過節點j走下去的花費
                    a_ex = [ x for x in xrange(1,n) if j != x and x in ap ]  
                    if m > euclidean_distance( cityNode[i], cityNode[j] ) + D[j][ subsets.index( a_ex ) ]:
                        m = euclidean_distance( cityNode[i], cityNode[j] ) + D[j][ subsets.index( a_ex ) ]
                        mp = j

                D[i][ subsets.index(a) ] = m # 從節點i出發，走訪子集合a的最短距離 
                middle[i][ subsets.index(a) ] = mp # 從節點i出發，走訪子集a 所應選擇的中途點

    short = inf

    A = [ x for x in subsets if 0 not in x and len(x) ==( len(citys)-1 ) ] #不包含初始點的唯一最大子集合
    for a in A:
        for j in xrange(1,n): #所有節點扣掉一個中途點的子集合，看看以此從起始點透過該中途點走下去的cost是否最低
            a_ex = [ x for x in a if j != x ] 
            if  short > euclidean_distance( cityNode[0], cityNode[j] ) + D[j][ subsets.index(a_ex) ]:
                short = euclidean_distance( cityNode[0], cityNode[j] ) + D[j][ subsets.index(a_ex) ]
                middle[0][ subsets.index(a) ] = j 
                D[0][subsets.index(a)] = short

    print 'shortest path: ', short
    showPath( D, middle, subsets )

def showPath( D, middle, subsets ):
    path = []
    startNode = 0 #從節點0出發
    citys.remove( startNode )
    path.append(startNode) 


    while [] != citys: #直到所有節點走完為止，重複尋找現有節點集合中，有最小花費的節點
        startNode = middle[startNode][ subsets.index( citys ) ] #當前節點數量下，所應選擇的下一步
        path.append(startNode) 
        citys.remove(startNode) #扣掉當前節點
    path.append( path[0] )
    print path


    plt.plot( cityNode[:,0], cityNode[:,1], 'ko' )

    '''
        edge
    '''
    for i in xrange( len(cityNode ) ):
        for j in xrange(i+1, len(cityNode) ):
            plt.plot( [ cityNode[i,0], cityNode[j,0] ], [ cityNode[i,1], cityNode[j,1] ], '--k' )
    '''
        optimal edge path
    '''
    for i in xrange( len(path)-1 ):
        plt.plot( [ cityNode[ path[i], 0], cityNode[ path[i+1], 0] ], [ cityNode[ path[i], 1], cityNode[ path[i+1] ,1] ], '-r' )

    plt.xticks( range(-3, 6) )
    plt.yticks( range(-3, 6) )
    plt.show()

if __name__ == '__main__':
    tsp()
