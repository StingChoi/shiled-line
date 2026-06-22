// Set up Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCYIEuLo-XPorkXjR77mwpSN9lA-LKptrM",
  authDomain: "shiled-cert.firebaseapp.com",
  projectId: "shiled-cert",
  storageBucket: "shiled-cert.firebasestorage.app",
  messagingSenderId: "578580128769",
  appId: "1:578580128769:web:f0f28f96b9192eac2fcc00"
};

// Initialize Firebase only once
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// Export instances to global window object so app.js can use them
window.auth = firebase.auth();
window.db = firebase.firestore();
