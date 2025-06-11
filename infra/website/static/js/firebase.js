import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDrpGdzubjHrR1HrKBsbV26B0Qp7kwNoOg",
    authDomain: "trendsleuthai.firebaseapp.com",
    storageBucket: "trendsleuthai.firebasestorage.app",
    messagingSenderId: "369068841607",
    appId: "G-KBJVSP9F82"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Export functions
export async function loginWithGoogle() {
  try {
    const result = await signInWithPopup(auth, provider);
    const idToken = await result.user.getIdToken();
    console.log("ID Token:", idToken);

    // Store token in localStorage
    localStorage.setItem("firebase_id_token", idToken);

    // Redirect to Streamlit app
    window.location.href = "https://app.trendsleuth.ai/?token=" + idToken;

  } catch (error) {
    console.error("Error during login:", error);
  }
}

export function logout() {
  auth.signOut().then(() => {
    localStorage.removeItem("firebase_id_token");
    window.location.href = "/";
  });
}
