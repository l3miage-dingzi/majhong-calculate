from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.meld import Meld
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data import Tiles
from utils import calculateTilesUseful,array36ToString


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

# 返回计算的向听数
class ShantenResponse(BaseModel):
    shanten: int

# 返回计算的有效进张
class TilesUsefulResponse(BaseModel):
    tilesUseful: str


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
    return TilesUsefulResponse(tilesUseful=array36ToString(tilesUseful))
