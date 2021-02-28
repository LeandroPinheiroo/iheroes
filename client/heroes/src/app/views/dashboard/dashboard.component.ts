import { SocketService } from './../../service/socket-service';
import { Component, OnInit } from '@angular/core';
import { getStyle, hexToRgba } from '@coreui/coreui/dist/js/coreui-utilities';
import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';

@Component({
  templateUrl: 'dashboard.component.html',
  styleUrls:['dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(
    private socketService: SocketService
  ) {
    
  }

  ngOnInit(){
    this.socketService.setConect();
    this.socketService.listen().subscribe((data)=>{
      console.log(data);
    })
  }


}
