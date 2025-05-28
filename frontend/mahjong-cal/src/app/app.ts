import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [CommonModule,FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  //protected title = 'mahjong-cal';
  protected tiles:string=''

  print(str:string){
    console.log(str)
  }

  getMPSZ(){
    
  }
}
