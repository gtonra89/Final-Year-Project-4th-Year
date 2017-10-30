import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

/*
  Generated class for the StatServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.

  This provider class will be used to make HTTP requests to stats API
*/
@Injectable()
export class StatServiceProvider {

  constructor(public http: Http) {
    console.log('Hello StatServiceProvider Provider');
  }

}
