from data import Tiles
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



def array36ToString(arr:list[int]):
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
    return string