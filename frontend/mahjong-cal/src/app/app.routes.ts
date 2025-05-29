import { Routes } from '@angular/router';
import { Shanten } from './shanten/shanten';

export const routes: Routes = [{path: 'home', component: Shanten},
    {path: '', redirectTo: '/home', pathMatch: 'full'}];
