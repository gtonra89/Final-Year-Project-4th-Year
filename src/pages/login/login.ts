import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ToastController } from 'ionic-angular';
import { SignupPage } from '../signup/signup';
import { AngularFireAuth } from 'angularfire2/auth';

@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  logData = {
    email: '',
    password: ''
  }

  constructor(public navCtrl: NavController, private afAuth: AngularFireAuth,private toastCtrl: ToastController) {
  
  }
  
  login() {
    // Login Code here
    this.afAuth.auth.signInWithEmailAndPassword(this.logData.email, this.logData.password)
    .then(auth => {
      // Do custom things with auth
    })
    .catch(err => {
      // Handle error// Handle error
      let toast = this.toastCtrl.create({
        message: err.message,
        duration: 3000
      });
      toast.present();
    });
  }
  

  /*
    The signup function redirects to the SignupPage and provides, 
    if available, the email address which was entered by the user inside the email field of the LoginPage. 
    In this case the user have not to reenter the email address on the SignupPage.
    */
  signup() {
    this.navCtrl.push(SignupPage, { email: this.logData.email });
    
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad LoginPage');
  }

}
