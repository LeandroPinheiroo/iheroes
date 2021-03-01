import * as io from 'socket.io-client'
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  socket:any;
  constructor(
  ) {  }

  setConect(){
    this.socket = io("https://zrp-challenge-socket.herokuapp.com");
  }
  

  listen(){
    return new Observable(observer => {
      this.socket.on('occurrence', msg => {
        observer.next(msg);
      });
    });
  }
}
