import { Router } from '@angular/router';
import { LogoutService } from './../../seguranca/logout.service';
import {Component} from '@angular/core';
import { navItems } from '../../_nav';

@Component({
  selector: 'app-dashboard',
  templateUrl: './default-layout.component.html'
})
export class DefaultLayoutComponent {
  public sidebarMinimized = false;
  public navItems = navItems;

  constructor(
    private logoutService: LogoutService,
    private router: Router
  ) {

  }

  toggleMinimize(e) {
    this.sidebarMinimized = e;
  }

  logout(): void {
    this.logoutService.logout()
      .then(() => {
         this.router.navigate(['/login']);
      })
      .catch();
  }
}
