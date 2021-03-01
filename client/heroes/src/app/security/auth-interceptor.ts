import { LoginService } from '../service/login-service';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, mergeMap } from 'rxjs/operators';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private auth: LoginService) {  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    if (req.url.includes('/oauth/token')) { return next.handle(req); }

    return next.handle(req).pipe(
      catchError(error => {
        if (error.status === 401) {
          return this.auth.refreshToken().pipe(
            mergeMap((newToken: string) => {
              req = req.clone({ setHeaders: { Authorization: `Bearer ${newToken}`}});
              return next.handle(req);
            })
          );
        }
        return throwError(error);
      })
    );
  }
}
