import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { HeroService } from './../../../service/hero-service';
import { NgForm } from '@angular/forms';
import { Hero } from './../../../domain/hero';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-hero-create',
  templateUrl: './hero-create.component.html',
  styleUrls: ['./hero-create.component.scss']
})
export class HeroCreateComponent implements OnInit {

  @ViewChild('form', {static: false}) form: NgForm;

  hero:Hero = new Hero();
  subscription: Subscription;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private heroSerive:HeroService,
    private toastrService: ToastrService
  ) { }

  ngOnInit(): void {
    this.subscription = this.route.params.subscribe((params) => {
      this.hero.id = params['id'];
      if(this.hero.id != null){
          this.findHero();
      }
  });
  }

  findHero(){
    return this.heroSerive.findById(this.hero.id)
      .subscribe( (response: Hero) => {
        console.log(response);
        this.hero = response;
      },
      erro => {
        this.toastrService.error(`Erro ao buscar o Herói ${this.hero.id}!`,'Erro!');
      }
    );
  }

  update(){
    return this.heroSerive.update(this.hero)
      .subscribe( () => {
        this.toastrService.success('Herói Atualizado com sucesso!','Sucesso!');
        return this.router.navigate(['/hero']);
      },
      erro => {
        this.toastrService.error(`Erro ao atualizar o Herói ${this.hero.name}!`,'Erro!');
      }
    );
  }

  create(){
    return this.heroSerive.create(this.hero)
      .subscribe( () => {
        this.toastrService.success('Herói Cadastrado com sucesso!','Sucesso!');
        return this.router.navigate(['/hero']);
      },
      erro => {
        this.toastrService.error(`Erro ao cadastrar o Herói ${this.hero.name}!`,'Erro!');
      }
    );
  }

  save(){
    if(this.form.invalid){
      return this.toastrService.error('Necessário preencher os campos obrigatórios!','Atenção!');
    }
    if(this.hero.id){
      return this.update();
    }
    return this.create();
  }

}
