import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal, Signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Score, Tiles } from '../data/data';
import { stringTotiles } from '../service/commun.service';
import { CalculateService } from '../service/calculate.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { catchError } from 'rxjs';
import { table } from 'node:console';

@Component({
  selector: 'app-shanten',
  imports: [CommonModule,FormsModule,HttpClientModule],
  templateUrl: './shanten.html',
  styleUrl: './shanten.css',
  providers:[CalculateService]
})
export class Shanten {
  cal=inject(CalculateService)
  //输入的手牌
  protected tilesStr=signal<string>('')
  protected tiles=computed<Tiles>(()=>stringTotiles(this.tilesStr()))
  protected tilesKnownStr=signal<string>('')
  tilesKnown=computed<Tiles>(()=>stringTotiles(this.tilesKnownStr()))
  //向听数
  shanten=signal<number>(-1)
  tilesUseful=signal<string>('')
  scores=signal<Score[]>([])
  api='http://localhost:8000'

  print(){
    console.log(this.tiles())
  }

  setTilesStr(str:string){
    this.tilesStr.set(str)
    //this.print()
  }

  calculateShanten(){
    this.cal.calculateSomething(this.tiles(), `${this.api}/shanten`).subscribe(data => {
      try {
        const shantenValue = (data as { shanten: number }).shanten;
        this.shanten.set(shantenValue);
      } catch (e) {
        console.error('处理结果时出错：', e);
      }
    });
    this.cal.calculateSomething(this.tiles(), `${this.api}/tilesUseful`).subscribe(data => {
      try {
        const tilesValue = (data as { tilesUseful: string }).tilesUseful;
        this.tilesUseful.set(tilesValue);
      } catch (e) {
        console.error('处理结果时出错：', e);
      }
    });
  }

  calculateDecision(){
    const request={hand:this.tiles(),table:this.tilesKnown()}
    this.cal.calculateSomething(request, `${this.api}/decision`).subscribe(data => {
      try {
        const scores = (data as { scores: Score[] }).scores;
        this.scores.set(scores)
        console.log(this.scores())
      } catch (e) {
        console.error('处理结果时出错：', e);
      }
    });
  }


}
