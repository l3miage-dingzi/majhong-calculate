from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.meld import Meld
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import array34ToString, calculateDecision, calculateTilesUnknown, calculateTilesUseful


calculator = HandCalculator()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HandRequest(BaseModel):
    m: str   # 万子，如 "123"
    p: str   # 筒子，如 "456"
    s: str   # 索子，如 "789"
    z: str  # 字牌，如 "1122"（东东南南）

class DecisionRequest(BaseModel):
    hand: HandRequest
    table: HandRequest

# 返回计算的向听数
class ShantenResponse(BaseModel):
    shanten: int

# 返回计算的有效进张
class TilesUsefulResponse(BaseModel):
    tilesUseful: str

class InfoScore(BaseModel):
    score:float
    shanten:int
    n:int
    tilesUseful:str

class Score(BaseModel):
    tile:str
    score:InfoScore

# 返回舍牌及分数
class ScoresResponse(BaseModel):
    scores: list[Score]


# useful helper
def print_hand_result(hand_result: HandResponse) -> None:
    print(hand_result.han, hand_result.fu)
    print(hand_result.cost["main"])
    print(hand_result.yaku)
    for fu_item in hand_result.fu_details:
        print(fu_item)
    print("")




@app.post("/shanten", response_model=ShantenResponse)
async def calculate_shanten(hand: HandRequest):
    # 将字符串转为34张牌数组（mahjong库方法）
    tiles = TilesConverter.string_to_34_array(
        man=hand.m,
        pin=hand.p,
        sou=hand.s,
        honors=hand.z,
    )
    # 计算向听数
    shanten = Shanten().calculate_shanten(tiles)
    return ShantenResponse(shanten=shanten)


@app.post("/tilesUseful", response_model=TilesUsefulResponse)
async def calculate_tilesUseful(hand: HandRequest):
    # 将字符串转为34张牌数组（mahjong库方法）
    tiles = TilesConverter.string_to_34_array(
        man=hand.m,
        pin=hand.p,
        sou=hand.s,
        honors=hand.z,
    )
    # 计算有效进张
    tilesUseful = calculateTilesUseful(tiles)
    return TilesUsefulResponse(tilesUseful=array34ToString(tilesUseful))


@app.post("/decision", response_model=ScoresResponse)
async def calculate_tilesUseful(des:DecisionRequest):
    hand=des.hand
    table=des.table
    # 将字符串转为34张牌数组（mahjong库方法）
    tiles = TilesConverter.string_to_34_array(
        man=hand.m,
        pin=hand.p,
        sou=hand.s,
        honors=hand.z,
    )
    tilesKnown=TilesConverter.string_to_34_array(
        man=table.m,
        pin=table.p,
        sou=table.s,
        honors=table.z,     
    )
    for i in range(34):
        tilesKnown[i]+=tiles[i]
    # 计算舍牌分数
    scores = calculateDecision(tiles,calculateTilesUnknown(tilesKnown))
    
    '''
    for t in scores:
        print(t.numTile)
        print(t.score)
    '''    
    
    scoresReturn:list[Score]=[]
    for s in sorted(scores, key=lambda s: s.score.score, reverse=True)[:3]:
        scoresReturn.append(Score(
            tile=array34ToString([s.numTile]),
            score={
                "score": s.score.score,
                "shanten": s.score.shanten,
                "n": s.score.n,
                "tilesUseful": s.score.tilesUseful
            }
        ))

    return ScoresResponse(scores=scoresReturn) 