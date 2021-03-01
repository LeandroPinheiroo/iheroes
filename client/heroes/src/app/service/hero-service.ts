import { Threat } from './../domain/threat';
import { Table } from 'primeng/table';
import { Hero } from './../domain/hero';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RequestUtil } from '../util/request-util';

@Injectable({
  providedIn: 'root'
})
export class HeroService {

  heroUrl = 'http://localhost:8080/api/hero';

  constructor(
      private http: HttpClient,
  ) {
  }

  findAll(table:Table) {
    const params: HttpParams = RequestUtil.getRequestParams(table);
    return this.http.get(this.heroUrl, RequestUtil.getHttpOptions());
  }

  getAll() {
    return this.http.get(`${this.heroUrl}/find-all`, RequestUtil.getHttpOptions());
  }

  findById(id:number) {
    return this.http.get(`${this.heroUrl}/${id}`, RequestUtil.getHttpOptions());
  }

  findHeroDefend(threat:Threat) {
    return this.http.post(`${this.heroUrl}/defend`, threat ,RequestUtil.getHttpOptions());
  }

  create(hero:Hero) {
    return this.http.post(this.heroUrl, hero, RequestUtil.getHttpOptions());
  }

  update(hero:Hero) {
    return this.http.put(this.heroUrl, hero, RequestUtil.getHttpOptions());
  }

  delete(id:number) {
    return this.http.delete(`${this.heroUrl}/${id}`,RequestUtil.getHttpOptions());
  }
}
