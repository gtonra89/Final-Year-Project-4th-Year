import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';
import { AngularFireModule } from 'angularfire2';
import { AngularFireAuthModule } from 'angularfire2/auth';
import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import { LoginPage } from '../pages/login/login';
import { SignupPage } from '../pages/signup/signup';
import { StatServiceProvider } from '../providers/stat-service/stat-service';
import { HttpClientModule } from '@angular/common/http'

var config = {
  apiKey: "AIzaSyCge-RN6-IkLdAbLkpkVkSnmkKpX1LkHkw",
  authDomain: "statflow-9c17a.firebaseapp.com",
  databaseURL: "https://statflow-9c17a.firebaseio.com",
  projectId: "statflow-9c17a",
  storageBucket: "",
  messagingSenderId: "163683249672"
};

@NgModule({
  declarations: [
    MyApp,
    HomePage,
    LoginPage,
    SignupPage
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    IonicModule.forRoot(MyApp),
    AngularFireModule.initializeApp(config),
    AngularFireAuthModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    LoginPage,
    SignupPage

  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    StatServiceProvider
  ]
})
export class AppModule {}
