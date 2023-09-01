import { initializeApp } from "firebase/app";
import { getDatabase} from "firebase/database";

const firebaseConfig = {
    apiKey: "AIzaSyAlnnZo7Lm2lMDVzFjOUsovZL9cfpeFEVY",
    authDomain: "baybin-project.firebaseapp.com",
    databaseURL: "https://baybin-project-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "baybin-project",
    storageBucket: "baybin-project.appspot.com",
    messagingSenderId: "25254133300",
    appId: "1:25254133300:web:411a031c53deb9dec59461",
    measurementId: "G-WXEEG63GZ9"
  };

const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);


