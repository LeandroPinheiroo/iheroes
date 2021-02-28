import { ToastrService } from 'ngx-toastr';
import { HeroService } from './../../../service/hero-service';
import { Hero } from './../../../domain/hero';
import { NgForm } from '@angular/forms';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Table } from 'primeng/table';

@Component({
  selector: 'app-hero-list',
  templateUrl: './hero-list.component.html',
  styleUrls: ['./hero-list.component.scss']
})
export class HeroListComponent implements OnInit {

  @ViewChild('form', {static: false}) form: NgForm;
  @ViewChild("table", {static: false}) datatable: Table;

  heroes:Hero[] = [];
  displayDialogConfirm:boolean = false;
  heroSelected:Hero = new Hero();

  constructor(
    private heroService:HeroService,
    private toastrService: ToastrService
  ) { }

  ngOnInit(): void {
  }

  search() {
    this.heroService.findAll(this.datatable)
      .subscribe((response:any) => {
          this.heroes = response.content;
      });
  }

  checkDelete(hero:Hero){
    this.heroSelected = hero;
    this.displayDialogConfirm = true;
  }

  clearDelete(){
    this.heroSelected = new Hero();
    this.displayDialogConfirm = false;
  }

  delete() {
    this.heroService.delete(this.heroSelected.id)
      .subscribe(() => {
        this.clearDelete();
        this.search();  
        this.toastrService.success('Herói apagado com sucesso!','Sucesso!');
      });
  }
  

}
