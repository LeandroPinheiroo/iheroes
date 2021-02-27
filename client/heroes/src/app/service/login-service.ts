import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

    loginUrl = 'http://localhost:8080/oauth/token';
    jwtPayload: any;

    constructor(private http: HttpClient,
                private jwtHelper: JwtHelperService) {

        this.loadToken();
    }

    loadToken() {
        const token = localStorage.getItem('token');

        if (token) {
        this.setToken(token);
        }
    }

    setToken(token: string) {
        this.jwtPayload = this.jwtHelper.decodeToken(token);
        localStorage.setItem('token', token);
    }

    login(usuario: string, password: string) {
        const httpOptions = {
            headers: new HttpHeaders({
            'Content-Type':  'application/x-www-form-urlencoded',
            'Authorization': 'Basic YW5ndWxhcjpAbmd1bEByMA=='
            }),
        withCredentials: true
        };
        const body = `username=${usuario}&password=${password}&grant_type=password`;
        return this.http.post(this.loginUrl, body, httpOptions);
    }

    getNewToken() {
        const httpOptions = {
        headers: new HttpHeaders({
            'Content-Type':  'application/x-www-form-urlencoded',
            'Authorization': 'Basic YW5ndWxhcjpAbmd1bEByMA=='
            }),
            withCredentials: true
        };

    const body = 'grant_type=refresh_token';

    return this.http.post(this.loginUrl, body, httpOptions)
        .subscribe((data: any) => {
            this.setToken(data.access_token);

            return Promise.resolve(null);
        },
        erro => {
            return Promise.resolve(null);
    });
  }


    isAccessTokenInvalido() {
        const token = localStorage.getItem('token');

        return !token || this.jwtHelper.isTokenExpired(token);
    }

    refreshToken(): Observable<string> {
        const headers = new HttpHeaders()
            .set('Content-Type', 'application/x-www-form-urlencoded')
            .set('Authorization', 'Basic YW5ndWxhcjpAbmd1bEByMA==');

        const params = new HttpParams().set('grant_type', 'refresh_token');

        return this.http.post(this.loginUrl, null, { headers, params, withCredentials: true })
            .pipe(
                map((token: any) => {
                this.setToken(token.access_token);
                return token.access_token;
                })
            );
    }

    clearAccessToken() {
        localStorage.removeItem('token');
        this.jwtPayload = null;
        console.log('limpou===');
      }

}
