import { ToastrService } from 'ngx-toastr';
import { LoginService } from './../../service/login-service';
import { Router } from '@angular/router';
import { UserService } from './../../service/user-service';
import { User } from './../../domain/user';
import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'register.component.html'
})
export class RegisterComponent {

  @ViewChild('form', {static: false}) form: NgForm;

  user: User = new User();

  constructor(
    private router: Router,
    private userService:UserService,
    private toastrService: ToastrService
  ) { }


  register() {
    if(this.form.invalid){
      return this.toastrService.error('Necessário preencher os campos obrigatórios!','Atenção!');
    }
    return this.userService.create(this.user)
      .subscribe( (log: any) => {
        this.toastrService.success('Cadastrado com sucesso, efetue o login!','Sucesso!');
        this.router.navigate(['/login']);
      },
      erro => {
        this.toastrService.error('Ocorreu um erro o se cadastrar!','Erro!');
      }
    );
  }

}
