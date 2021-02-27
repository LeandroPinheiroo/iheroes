import { LoginService } from './../../service/login-service';
import { Router } from '@angular/router';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { User } from '../../domain/user';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'login.component.html'
})
export class LoginComponent implements OnInit {
  @ViewChild('form', {static: false}) form: NgForm;

  user: User = new User();

  constructor(
    private router: Router,
    private loginService:LoginService,
    private toastrService: ToastrService
  ) { }


  ngOnInit(){
   
  }

  register(){
    this.router.navigate(['register']);
  }

  login() {
    if(this.form.invalid){
      return this.toastrService.error('Necessário preencher os campos obrigatórios!','Atenção!');
    }
    return this.loginService.login(this.user.email, this.user.password)
      .subscribe( (log: any) => {
        this.loginService.setToken(log.access_token);
        this.router.navigate(['/']);
      },
      erro => {
        this.toastrService.error('Verifique suas credênciais!','Erro!');
      }
    );
  }


}
