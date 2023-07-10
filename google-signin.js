// Google Sign-In button click event handler
function handleGoogleSignIn() {

  google.accounts.id.initialize({

    // client_id: '',

    callback: handleGoogleSignInCallback

  });

  google.accounts.id.prompt();

}

// Google Sign-In callback function

function handleGoogleSignInCallback(response) {

  if (response.credential) {

    const credential = firebase.auth.GoogleAuthProvider.credential(response.credential);

    firebase.auth().signInWithCredential(credential)

      .then((userCredential) => {

        // Redirect the user to the home page or a success page

        window.location.href = 'index.html';

      })

      .catch((error) => {

        // Handle any errors that occur during sign-in

        alert(error.message);

      });

  }

}

