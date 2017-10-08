import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController } from 'ionic-angular';
import { AngularFireAuth } from 'angularfire2/auth';
/**
 * Generated class for the SignupPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-signup',
  templateUrl: 'signup.html',
})
export class SignupPage {
  
  signupInfo = {
    email: '',
    password: '',
    confirmPassword: ''
  };

  constructor(
    private navCtrl: NavController,
    private navParams: NavParams,
    private alertCtrl: AlertController,
    private afAuth: AngularFireAuth) {
	    this.signupInfo.email = this.navParams.get('email');
	  }

  signup() {
    if(this.signupInfo.password !== this.signupInfo.confirmPassword) {
      let alert = this.alertCtrl.create({
            title: 'Error',
            message: 'Your passwords do not match each other.',
            buttons: ['Retry']
      });
      alert.present();
      return;
    }
    this.afAuth.auth.createUserWithEmailAndPassword(this.signupInfo.email, this.signupInfo.password)
    .then(auth => {
      // Could do something with the Auth-Response
      console.log(auth);
    })
    .catch(err => {
      // Handle error
      let alert = this.alertCtrl.create({
        title: 'Error',
        message: err.message,
        buttons: ['Retry']
      });
      alert.present();
    });

  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SignupPage');
  }

}
