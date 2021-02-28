import { ToastrService } from 'ngx-toastr';
import { Hero } from './../../domain/hero';
import { HeroService } from './../../service/hero-service';
import { Threat } from './../../domain/threat';
import { SocketService } from './../../service/socket-service';
import { Component, OnInit } from '@angular/core';
import { getStyle, hexToRgba } from '@coreui/coreui/dist/js/coreui-utilities';
import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';

@Component({
  templateUrl: 'dashboard.component.html',
  styleUrls:['dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  threat:Threat = new Threat();
  hero:Hero = new Hero();

  constructor(
    private socketService: SocketService,
    private heroService: HeroService,
    private toastrService: ToastrService
  ) {
    
  }

  ngOnInit(){
    this.socketService.setConect();
    this.socketService.listen().subscribe((data:any)=>{
      this.preparesThreat(data);
      this.findHero();
    })
  }

  preparesThreat(data){
    this.threat.location.lat = data.location[0].lat
    this.threat.location.lng = data.location[0].lng
    this.threat.dangerLevel = data.dangerLevel;
    this.threat.monsterName = data.monsterName;
    console.log(this.threat);
  }



  findHero(){
    return this.heroService.findHeroDefend(this.threat)
      .subscribe( (response: Hero) => {
        this.hero = response;
        console.log(this.hero);
      },
      erro => {
        this.toastrService.error(`Erro ao buscar o Herói para deter a ameaça ${this.threat.monsterName}!`,'Erro!');
      }
    );


  }





}
