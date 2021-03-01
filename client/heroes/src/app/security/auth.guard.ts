import { LoginService } from '../service/login-service';
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private auth: LoginService,
    private router: Router
   ) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

      if (this.auth.isAccessTokenInvalido()) {
        console.log('Navegação com access token inválido. Obtendo novo token...');

        this.auth.getNewToken();
        if (this.auth.isAccessTokenInvalido()) {
              this.router.navigate(['/login']);
              return false;
        }
      }
     return true;
  }
}
