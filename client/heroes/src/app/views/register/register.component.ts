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
    private userService:UserService
  ) { }


  register() {
    console.log(this.user);
    return this.userService.create(this.user)
      .subscribe( (log: any) => {
        this.router.navigate(['/']);
      },
      erro => {
        console.log("error")
      }
    );
  }

}
