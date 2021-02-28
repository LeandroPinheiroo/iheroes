import { HeroListComponent } from './hero-list/hero-list.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HeroCreateComponent } from './hero-create/hero-create.component';


const routes: Routes = [
  {
    path: '',
    component: HeroListComponent,
    data: {
      title: 'Listagem de Heróis'
    }
  },
  {
    path: 'create',
    component: HeroCreateComponent,
    data: {
      title: 'Herói'
    }
  },
  {
    path: 'update/:id',
    component: HeroCreateComponent,
    data: {
      title: 'Herói'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HeroRoutingModule {}
