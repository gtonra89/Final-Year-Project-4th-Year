import { Injectable } from '@angular/core';
//import { HTTP } from '@ionic-native/http';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

/*
  Generated class for the StatServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.

  This provider class will be used to make HTTP requests to stats API
*/

/*
 * Issue with HTTP. ionic 3 is still using old Angular http module. 
 * https://www.djamware.com/post/59924f9080aca768e4d2b12e/ionic-3-consuming-rest-api-using-new-angular-43-httpclient
 * Install new http module for angular 4
 */
@Injectable()
export class StatServiceProvider {
   data: any; //data is set to any data. Used for stats data
   apiKey = 'e73247acc1634ff3835f66aaa3de7745';
//==== Constructor =============================
  constructor(private http: Http) {
    console.log('Hello StatServiceProvider Provider');
    // Just using our own data sample at first just to get things running
    //json format
    this.data;
  }
// Load method will be used to get the api data and load it in
  load(){
      //if(this.data){
      //return Promise.resolve(this.data);
    //} 
    //dont have data yet..
    return new Promise(resolve => {
      //API request
      this.http.get('http://api.football-data.org/v1/teams/66')
      .map(res => res.json())
      .subscribe(data => {
        this.data = data;
        resolve(data);
      });
    });
    
  } //end of load()

} //end of class
