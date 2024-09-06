const emailInput = document.getElementById("id_email");
const firstName = document.getElementById("id_first_name");
const lastName = document.getElementById("id_last_name");

const hidepass = document.querySelector('#hidepass')
const showpass = document.querySelector('#showpass')

const hidepass1 = document.querySelector('#hidepass1')
const showpass1 = document.querySelector('#showpass1')

const hidepass2 = document.querySelector('#hidepass2')
const showpass2 = document.querySelector('#showpass2')

// capitalize first letters of words
function capitalizeFirstLetter(input,inputField) {
    // Split the string into an array of words
    let words = input.split(' ');

    // Capitalize the first letter of each word
    let capitalizedWords = words.map(word => {
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    });

    // Join the array back into a string
    let capitalizedString = capitalizedWords.join(' ');

    // Optionally, set the modified string back to the form input
    inputField.value = capitalizedString;
}

// capitalizing both first name and lastname in input field
if (firstName) {
    firstName.addEventListener("input", e => capitalizeFirstLetter(e.target.value, firstName));
}
if (lastName) {
    lastName.addEventListener("input", e => capitalizeFirstLetter(e.target.value, lastName));
}


// Converting email input to lowerCase
emailInput.addEventListener("input", function() {
    this.value = this.value.toLowerCase().trim();
});

// login show and hide passwords with icons
const showpassword = (e => {
    console.log('god is good');
    const passwordfield = document.querySelector('input[name=password]');

    if (passwordfield.type === 'password') {
        showpass.style.visibility = "hidden"
        hidepass.style.visibility = "visible";
        passwordfield.type = 'text';

    } else {
        hidepass.style.visibility = "hidden";
        showpass.style.visibility = "visible";
        passwordfield.type = "password";
    }
})
// register
const showpassword1 = (e => {
    const passwordfield1 = document.querySelector('input[name=password1]');

    if (passwordfield1.type === 'password') {
        showpass1.style.visibility = "hidden"
        hidepass1.style.visibility = "visible";
        passwordfield1.type = 'text';
    } else {
        hidepass1.style.visibility = "hidden";
        showpass1.style.visibility = "visible";
        passwordfield1.type = "password";
    }

})

const showpassword2 = (e => {
    console.log('god is good');
    const passwordfield2 = document.querySelector('input[name=password2]');

    if (passwordfield2.type === 'password') {
        showpass2.style.visibility = "hidden"
        hidepass2.style.visibility = "visible";
        passwordfield2.type = 'text';
    } else {
        hidepass2.style.visibility = "hidden";
        showpass2.style.visibility = "visible"
        passwordfield2.type = "password";
    }
})

// remove alert btn
function removeAlert() {
    const btn = document.querySelector(".message-alert");
    btn.classList.add("remove-alert")
}