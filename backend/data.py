class Tiles:
    def __init__(self, m: str, p: str, s: str, z: str):
        self.m = m  # 万子
        self.p = p  # 筒子
        self.s = s  # 条子
        self.z = z  # 字牌

class InfoScore:
    def __init__(self,score:float,shanten:int,n:int,tilesUseful:str):
        self.score=score
        self.shanten=shanten
        self.n=n
        self.tilesUseful=tilesUseful

class Score:
    def __init__(self, numTile:int,score:InfoScore):
        self.numTile=numTile
        self.score=score