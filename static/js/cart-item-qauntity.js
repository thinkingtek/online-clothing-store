const itemMinusbtn = document.querySelectorAll('#min-btn')
const itemPlusbtn = document.querySelectorAll('#plus-btn')


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const qminBtn = () => {
  return fetch("{% url 'cart:item-q-decrement' %}", {
      method: "post",
      // body: JSON.stringify(details),
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
  }
  })
}
const qPlusBtn = () => {
  return fetch("{% url 'cart:item-q-increment' %}", {
      method: "post",
      // body: JSON.stringify(details),
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
  }
  })
}

itemMinusbtn.forEach((btn) => {
  btn.addEventListener("click",e => {
    e.preventDefault()
  console.log("minus btn worked well")
  })
})
itemPlusbtn.forEach((btn) => {
  btn.addEventListener("click",e => {
    e.preventDefault()
  console.log("plus btn worked well")
  })
})

// itemMinusbtn.addEventListener('click', e => {
//   e.preventDefault()
//   console.log("minus btn worked well")
// })



// itemPlusbtn.addEventListener('click', e => {
//   e.preventDefault()
//   console.log("plus btn worked well")
// })





const plusBtn = (e) => {
  // e.preventDefault()
  console.log("it worked well")
}
// const minusBtn = (e) => {
  
//   preventDefault()
//   console.log("it worked well")
// }