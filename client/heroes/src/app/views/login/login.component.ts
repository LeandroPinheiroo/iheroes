import { LoginService } from './../../service/login-service';
import { Router } from '@angular/router';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { User } from '../../domain/user';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'login.component.html'
})
export class LoginComponent implements OnInit {
  @ViewChild('form', {static: false}) form: NgForm;

  user: User = new User();

  constructor(
    private router: Router,
    private loginService:LoginService
  ) { }


  ngOnInit(){
   
  }

  register(){
    this.router.navigate(['register']);
  }

  login() {
    return this.loginService.login(this.user.email, this.user.password)
      .subscribe( (log: any) => {
        this.loginService.setToken(log.access_token);
        this.router.navigate(['/']);
      },
      erro => {
        console.log("error")
      }
    );
  }


}
