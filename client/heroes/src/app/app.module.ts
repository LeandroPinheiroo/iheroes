import { HeroCreateComponent } from './views/hero/hero-create/hero-create.component';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { PerfectScrollbarModule } from 'ngx-perfect-scrollbar';
import { PERFECT_SCROLLBAR_CONFIG } from 'ngx-perfect-scrollbar';
import { PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
import { ToastrModule } from 'ngx-toastr';


import { IconModule, IconSetModule, IconSetService } from '@coreui/icons-angular';

import { JwtHelperService, JwtModule } from '@auth0/angular-jwt';

const DEFAULT_PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
  suppressScrollX: true
};

import { AppComponent } from './app.component';

// Import containers
import { DefaultLayoutComponent } from './containers';

import { P404Component } from './views/error/404.component';
import { P500Component } from './views/error/500.component';
import { LoginComponent } from './views/login/login.component';
import { RegisterComponent } from './views/register/register.component';

const APP_CONTAINERS = [
  DefaultLayoutComponent
];

import {
  AppAsideModule,
  AppBreadcrumbModule,
  AppHeaderModule,
  AppFooterModule,
  AppSidebarModule,
} from '@coreui/angular';

// Import routing module
import { AppRoutingModule } from './app.routing';

// Import 3rd party components
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { ChartsModule } from 'ng2-charts';
import { HttpClientModule } from '@angular/common/http';
import { HeroModule } from './views/hero/hero.module';

export function tokenGetter() {
  return localStorage.getItem('token');
}

@NgModule({
  imports: [
    FormsModule,
    HttpClientModule,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    AppAsideModule,
    AppBreadcrumbModule.forRoot(),
    AppFooterModule,
    AppHeaderModule,
    AppSidebarModule,
    PerfectScrollbarModule,
    ToastrModule.forRoot(),
    BsDropdownModule.forRoot(),
    TabsModule.forRoot(),
    ChartsModule,
    IconModule,
    IconSetModule.forRoot(),
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        whitelistedDomains: [
          'localhost:4200',
          'localhost:8080'
        ],
        blacklistedRoutes: [
          'http://localhost:8080/oauth/token'
        ],
        skipWhenExpired: true
      }
    }),
    HeroModule
  ],
  declarations: [
    AppComponent,
    ...APP_CONTAINERS,
    P404Component,
    P500Component,
    LoginComponent,
    RegisterComponent
  ],
  providers: [
    JwtHelperService,
    {
      provide: LocationStrategy,
      useClass: HashLocationStrategy
    },
    IconSetService,
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
