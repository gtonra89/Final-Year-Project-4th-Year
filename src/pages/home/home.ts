import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import {AngularFireAuth }from 'angularfire2/auth';
import { StatServiceProvider } from '../../providers/stat-service/stat-service';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
  // variable for players
  teams: any;

  //======= Constructor ==================================================
  constructor(public navCtrl: NavController, private auth: AngularFireAuth, public StatServiceProvider: StatServiceProvider) {
    //passing in api data from providers 
   // this.StatServiceProvider.load().then(data => {
      //this.teams = data; //storing it into players
   // });
    this.getTeams();

  } //end constructor


  signOut() {
    this.auth.auth.signOut();
  }

  getTeams() 
  {
    this.StatServiceProvider.load()
    .then(data => {
      this.teams = data;
     // console.log(this.teams);
    });

  }//end getTeams


}//end HomePage Class
