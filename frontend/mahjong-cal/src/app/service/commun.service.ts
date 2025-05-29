import { Injectable } from '@angular/core';
import { Tiles } from '../data/data';

@Injectable({
  providedIn: 'root'
})
export class CommunService {




}
export function tilesToString(){
    
}  



//将string转换为Tiles
export function stringTotiles(str:string):Tiles{
  const mList:string[]=[]
  const pList:string[]=[]
  const sList:string[]=[]
  const zList:string[]=[]

  for(let i=0;i<str.length;i+=2){
    const num=str[i]
    const type=str[i+1]
    //判断牌的种类
    if(type==='m'){
      mList.push(num)
    }else if(type==='p'){
      pList.push(num)
    }else if(type==='s'){
      sList.push(num)
    }else if(type==='z'){
      zList.push(num)
    }
  }
  return {
    m: mList.join(''),
    p: pList.join(''),
    s: sList.join(''),
    z: zList.join(''),
  }

}