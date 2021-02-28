import { FormsModule } from '@angular/forms';
import { HeroRoutingModule } from './hero-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeroCreateComponent } from './hero-create/hero-create.component';
import { HeroListComponent } from './hero-list/hero-list.component';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
import {DialogModule} from 'primeng/dialog';


@NgModule({
  declarations: [HeroCreateComponent, HeroListComponent],
  imports: [
    HeroRoutingModule,
    CommonModule,
    TableModule,
    FormsModule,
    InputTextModule,
    ButtonModule,
    TooltipModule,
    DialogModule
  ]
})
export class HeroModule { }
