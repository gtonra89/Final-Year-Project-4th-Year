import { Injectable } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import 'rxjs/add/operator/map';

/*
  Generated class for the StatServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.

  This provider class will be used to make HTTP requests to stats API
*/
@Injectable()
export class StatServiceProvider {
   data: any;

  constructor(public http: HttpClientModule) {
    console.log('Hello StatServiceProvider Provider');
    this.data = [ 
      {name: 'Ronaldo', goals: 300, club: 'Real Madrid'},
      {name: 'Messi', goals: 300, club: 'Barcelona'}
    ];
  }

  load(){
    /*if(this.data){
      return Promise.resolve(this.data);
    }
    //dont have data yet..
    return new Promise(resolve => {
      this.http.get('https://randomuser.me/api/?results=10')
      .map(res => res.json())
      .subscribe(data => {
        this.data = data.results;
        resolve(this.data);
      });
    }); */
    if(this.data){

    
    return Promise.resolve(this.data);
    }
  }

}
