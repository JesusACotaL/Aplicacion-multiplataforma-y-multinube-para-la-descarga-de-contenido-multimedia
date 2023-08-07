// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  firebase: {
    projectId: 'mango-ec7e1',
    appId: '1:608745411249:web:b0f8c57f55a06e33260890',
    storageBucket: 'mango-ec7e1.appspot.com',
    apiKey: 'AIzaSyBdtAVOOUTnmfycmPexnI0f1Z-WUw_7Pe8',
    authDomain: 'mango-ec7e1.firebaseapp.com',
    messagingSenderId: '608745411249',
  },
  production: false,
  mainMangaAPI: "http://192.168.1.12:5000"
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
