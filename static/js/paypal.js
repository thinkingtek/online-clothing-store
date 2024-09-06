const loader = document.querySelector(".paypal-spinner");
const failedTrans = document.querySelector(".failed-trans");
const successTrans = document.querySelector(".success-trans");
const paymentInfo = document.querySelector(".payment-info");
const msgAlert = document.querySelector(".message-alert");

// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//     const cookies = document.cookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//       // Does this cookie string begin with the name we want?
//       if (cookie.substring(0, name.length + 1) === (name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');

// const sendOrderConfirmed = (details) => {
//   return fetch("{% url 'cart:confirm-order' %}", {
//     method: "POST",
//     body: JSON.stringify(details),
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrftoken
//     }
//   })
// }

paypal.Buttons({
  createOrder: function (data, actions) {
    // Set up the transaction
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: '{{order.get_all_total}}', currency: 'NGN'
        }
      }]
    });
  },
  // onApprove: function (data, actions) {
  //   return actions.order.capture().then(function (details) {
  //     console.log("details is working");

  //   })

  // }
}).render('#paypal-button-container');


