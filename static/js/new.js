
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