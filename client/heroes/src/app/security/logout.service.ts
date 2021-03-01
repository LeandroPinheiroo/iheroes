import { LoginService } from '../service/login-service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  tokensRenokeUrl = 'http://localhost:8080/tokens/revoke';
  constructor(
      private http: HttpClient,
      private auth: LoginService
   ) { }

  logout() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/x-www-form-urlencoded',
        'Authorization': 'Basic YW5ndWxhcjpAbmd1bEByMA=='
      }),
      withCredentials: true
    };
    return this.http.delete(this.tokensRenokeUrl, httpOptions)
      .toPromise()
      .then(() => {
        this.auth.clearAccessToken();
      });
   }
}
