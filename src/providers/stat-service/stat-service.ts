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
   data: any; //data is set to any data. Used for stats data

//==== Constructor =============================
  constructor(public http: HttpClientModule) {
    console.log('Hello StatServiceProvider Provider');
    // Just using our own data sample at first just to get things running
    //json format
    this.data = [ 
      {name: 'Ronaldo', goals: 300, club: 'Real Madrid'},
      {name: 'Messi', goals: 300, club: 'Barcelona'}
    ];
  }
// Load method will be used to get the api data and load it in
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
      //return the data
    return Promise.resolve(this.data);
    }
  }

}
