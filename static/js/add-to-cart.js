const input = document.getElementById("id_quantity");
const stock = parseInt(document.getElementById("stock-count").innerText);


// decrease the quantity from the minimum
function btnMinus() {
    if (input.value > input.min) {
        input.value--;
    } else if (input.value == input.min) {
        return false
    }
}

// increase the quantity in based on the num of stock
function btnPlus() {
    if (input.value != stock) {
        input.value++;
    } else {
        return false
    }
}

// swipper
const galleryThumbs = new Swiper('.gallery-thumbs', {
    spaceBetween: 5,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
});

const galleryTop = new Swiper('.gallery-top', {
    spaceBetween: 10,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    thumbs: {
        swiper: galleryThumbs
    }
});