
const titleInput = document.querySelector('input[name=title]');
const slugInput = document.querySelector('input[name=slug]');
const catCheckboxes = document.getElementsByName('tags');
const tagCheckboxes = document.getElementsByName('categories');

const slugify = (val) => {

    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and-')         // Replace & with 'and'
        .replace(/[\s\W-]+/g, '-')      // Replace spaces, non-word characters and dashes with a single dash (-)

};

titleInput.addEventListener('keyup', (e) => {
    slugInput.setAttribute('value', slugify(titleInput.value));
    console.log('Working')
});



// checkbox validations for limit for categories and tags

const validateCheck = (e => {
    const errorcheckbox = document.querySelector('.error-category');
    let checkboxes = document.getElementsByName('categories');
    let numofChoices = 0
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            numofChoices++
        }
        if (numofChoices < 2) {
            errorcheckbox.style.display = "none"
        } else if (numofChoices > 2) {
            errorcheckbox.style.display = "block"
            return false
        }
    }
})

// checkbox validations for limit for tags
const validateCheckTag = (e => {
    const errorcheckbox = document.querySelector('.error-tag');
    let checkboxes = document.getElementsByName('tags');
    let numofChoices = 0
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            numofChoices++
        }
        if (numofChoices < 2) {
            errorcheckbox.style.display = "none"
        } else if (numofChoices > 2) {
            errorcheckbox.style.display = "block"
            return false
        }

    }
})
