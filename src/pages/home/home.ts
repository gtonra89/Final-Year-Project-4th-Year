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
  public players: any;

  //======= Constructor ==================================================
  constructor(public navCtrl: NavController, private auth: AngularFireAuth, public StatServiceProvider: StatServiceProvider) {
    //passing in api data from providers 
    this.StatServiceProvider.load().then(result => {
      this.players = result; //storing it into players
    });
  }


  signOut() {
    this.auth.auth.signOut();
  }

}
