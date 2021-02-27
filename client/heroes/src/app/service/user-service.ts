import { User } from './../domain/user';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({
  providedIn: 'root'
})
export class UserService {

    loginUrl = 'http://localhost:8080/api/user';
    jwtPayload: any;

    constructor(
        private http: HttpClient,
    ) {
    }

    create(user:User) {
        const httpOptions = {
            headers: new HttpHeaders({
              'Content-Type': 'application/json'
              },
            )
        };
        return this.http.post(this.loginUrl, user, httpOptions);
    }
}
