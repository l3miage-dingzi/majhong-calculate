export interface Tiles{
    m:string;//万子
    p:string;//筒子
    s:string;//条子
    z:string;//字牌
}

export interface Score{
    tile:string;
    score:InfoScore
}

export interface InfoScore{
    score:number
    shanten:number
    n:number
    tilesUseful:string
}