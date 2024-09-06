const date = new Date();
document.querySelector(".year-span").innerHTML = date.getFullYear();

const toggle = document.querySelector('.nav_toggle');
// toggle.addEventListener('click', e => {
//   console.log("it worked")
// })

toggle.addEventListener("click", (e) => {
  const body = document.getElementById('body-id');
  const sidebar = document.querySelector('.mobile_sidebar');
  if (sidebar) {
    sidebar.classList.toggle("show-sidebar");
    body.classList.toggle("body-overflow-hidden");
  }
})


// scrolltop
function showScroll() {
  const scrollTop = document.getElementById("scroll-top");
  if (this.scrollY >= 450) {
    scrollTop.classList.add("show-scroll");
  } else {
    scrollTop.classList.remove("show-scroll");
  }
}

function scrollToTop() {
  window.scroll({top:0,left:0,behavior:'smooth'});
}

window.addEventListener("scroll", showScroll);

// remove alert btn
function removeAlert() {
  const btn = document.querySelector(".message-alert");
  btn.classList.add("remove-alert")
}