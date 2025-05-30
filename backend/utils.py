import math
from data import InfoScore, Score
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.shanten import Shanten

calculator = HandCalculator()

def calculateTilesUseful(tilesArray:list[int]):
    tilesUsefulArray:list[int]=[]
    shantenCurrent = Shanten().calculate_shanten(tilesArray)
    for tile in range(34):
        if tilesArray[tile] >= 4:
            continue
        tilesArrayCopy=tilesArray.copy()
        tilesArrayCopy[tile] += 1
        if(shantenCurrent==0):    
            tilesArrayCopy136=TilesConverter.to_136_array(tilesArrayCopy)
            if calculator.estimate_hand_value(tilesArrayCopy136,tilesArrayCopy136[-1]).error is None:
                tilesUsefulArray.append(tile)     
        else:
            shantenWithNewTile=Shanten().calculate_shanten(tilesArrayCopy)
            if shantenWithNewTile<shantenCurrent:
                tilesUsefulArray.append(tile)
    return tilesUsefulArray



def array34ToString(arr:list[int]):
    string:str=''
    for ele in arr:
        a=ele//9 #判断种类
        b=ele%9  #判断数字
        if a==0:
            string+=(str(b+1)+'m')
        elif a==1:
            string+=(str(b+1)+'p')
        elif a==2:
            string+=(str(b+1)+'s')
        elif a==3:
            string+=(str(b+1)+'z')
        string+=' '
    string=string[:-1]
    return string


def calculateScore(tiles:list[int],tilesUnknown:list[int]):
    alpha:float=100
    beta:float=1.5
    k:float=0.446
    shanten=Shanten().calculate_shanten(tiles)
    tilesUseful=calculateTilesUseful(tiles)
    n:int=0
    for ele in tilesUseful:
        n+=tilesUnknown[ele]
    if shanten==0:
        score=alpha*math.exp(-k*shanten)+beta*n
    else:
        score=alpha*math.exp(-k*shanten)+beta*n/shanten
    print(alpha,beta,k,shanten,n)
    return InfoScore(score=score,shanten=shanten,n=n,tilesUseful=array34ToString(tilesUseful))


def calculateTilesUnknown(tilesKnown:list[int]):
    allTiles:list[int]=[4]*34
    for i in range(34):
        allTiles[i]-=tilesKnown[i]
    return allTiles

def calculateDecision(tiles:list[int],tilesUnknown:list[int]):
    scores:list[Score]=[]
    for i in range(34):
        if tiles[i]>0:
            tilesCopy=tiles.copy()
            tilesCopy[i]-=1
            scores.append(Score(i,calculateScore(tilesCopy,tilesUnknown)))  
    return scores

