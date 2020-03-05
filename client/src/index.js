import React from 'react';
import ReactDOM from 'react-dom';
import * as firebase from 'firebase/app';

import * as serviceWorker from './serviceWorker';
import './index.css';
import App from './App';

require('dotenv').config();

const firebaseConfig = {
    apiKey: process.env.API_KEY,
    authDomain: 'groundstation-ecf9f.firebaseapp.com',
    databaseURL: 'https://groundstation-ecf9f.firebaseio.com',
    projectId: 'groundstation-ecf9f',
    storageBucket: 'groundstation-ecf9f.appspot.com',
    messagingSenderId: process.env.FIREBASE_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID,
    measurementId: process.env.FIREBASE_MEASUREMENT_ID
};
firebase.initializeApp(firebaseConfig);

ReactDOM.render(<App firebase={firebase} />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
