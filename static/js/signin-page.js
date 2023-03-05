const signinForm = document.getElementById("signin-form");
const signinButton = document.getElementById("signin-form-submit");
const signinErrorMsgMatch = document.getElementById("signin-error-msg-match");
const signinErrorMsgTaken = document.getElementById("signin-error-msg-taken");

signinButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = signinForm.username.value;
    const password = signinForm.password.value;
    const pass_conf = signinForm.password_conf.value;

    if (password == pass_conf) {
        if (username == "user") {
            alert("You have successfully logged in.");
            location.reload();
        } 
        else {
            signinErrorMsgTaken.style.opacity = 1;
        }
    }
    else {
        signinErrorMsgMatch.style.opacity = 1;
    }
})