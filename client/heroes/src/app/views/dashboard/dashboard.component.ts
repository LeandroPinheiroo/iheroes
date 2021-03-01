import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { Hero } from './../../domain/hero';
import { HeroService } from './../../service/hero-service';
import { Threat } from './../../domain/threat';
import { SocketService } from './../../service/socket-service';
import { Component, OnInit } from '@angular/core';

@Component({
  templateUrl: 'dashboard.component.html',
  styleUrls:['dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  threat:Threat = new Threat();
  hero:Hero = new Hero();
  heroes:Hero[] = [];
  apiLoaded: Observable<boolean>;

  options: google.maps.MapOptions = {
    zoomControl: false,
    scrollwheel: false,
    disableDoubleClickZoom: true,
    zoom:2
  };
  markers = [];

  constructor(
    private socketService: SocketService,
    private heroService: HeroService,
    private toastrService: ToastrService,
  ) {}

  ngOnInit(){
    this.socketService.setConect();
    this.socketService.listen().subscribe((data:any)=>{
      this.preparesThreat(data);
      this.findHero();
    })
    this.getAllHeroes();
  }

  preparesThreat(data){
    this.threat.location.lat = data.location[0].lat
    this.threat.location.lng = data.location[0].lng
    this.threat.dangerLevel = data.dangerLevel;
    this.threat.monsterName = data.monsterName;
    this.addThreatMap();
  }

  getAllHeroes(){
    return this.heroService.getAll()
      .subscribe( (response: Hero[]) => {
        this.heroes = response;
        this.addHeroesMap();
      },
      erro => {
        this.toastrService.error(`Erro ao buscar os Heróis salvos!`,'Erro!');
      }
    );
  }

  addHeroesMap(){
    this.heroes.map(hero => {
      this.markers.push(
        {
          position: {
            lat: hero.location.lat,
            lng: hero.location.lng,
          },
          label: {
            color: 'blue',
            text: hero.name,
          },
          title: hero.enumHero,
          options: { animation: google.maps.Animation.DROP },
        }
      );
    });
    
  }

  addThreatMap(){
    this.markers.push({
      position: {
        lat: this.threat.location.lat ,
        lng: this.threat.location.lng
      },
      label: {
        color: 'red',
        text: this.threat.dangerLevel,
      },
      title: this.threat.monsterName,
      options: { animation: google.maps.Animation.BOUNCE },
    });
  }

  findHero(){
    return this.heroService.findHeroDefend(this.threat)
      .subscribe( (response: Hero) => {
        this.hero = response;
      },
      erro => {
        this.toastrService.error(`Erro ao buscar o Herói para deter a ameaça ${this.threat.monsterName}!`,'Erro!');
      }
    );
  }
}
