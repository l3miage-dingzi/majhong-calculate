import { HttpClient, HttpResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Tiles } from '../data/data';
import { catchError, EMPTY, map, switchMap, tap, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CalculateService {

  http=inject(HttpClient)

  calculateSomething(data:Tiles,api:string){
    return this.http.post(api,data,{ observe: 'response'}).pipe(
      map(r=>{
            if(r.ok){
            return r.body
          }else{
            throw new Error('error')
          }
      }),
      catchError(error=>{return throwError(()=>error)})
    )
  
  }
}
