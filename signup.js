const signupForm = document.getElementById('signup-form');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const termsCheckbox = document.getElementById('terms-checkbox');

// Add an event listener to the signup form
signupForm.addEventListener('submit', (e) => {
  e.preventDefault(); // Prevent the form from submitting by default

  const username = usernameInput.value;
  const email = emailInput.value;
  const password = passwordInput.value;
  const agreedToTerms = termsCheckbox.checked;

  // Validate the form inputs
  if (!username || !email || !password || !agreedToTerms) {
    alert('Please fill in all the required fields and agree to the terms.');
    return;
  }

  // Sign up the user with Firebase Authentication
  firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Update the user's display name
      const user = userCredential.user;
      return user.updateProfile({
        displayName: username
      });
    })
    .then(() => {
      // Redirect the user to the home page or a success page
      window.location.href = 'home.html';
    })
    .catch((error) => {
      // Handle any errors that occur during signup
      alert(error.message);
    });
});
