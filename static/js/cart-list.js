// Money/currency formatter
const formatter = new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN',
    minimumFractionDigits:2,
    maximumFractionDigits: 2
});

// Upadate total price after changing the shipping method
async function updateTotalPrice(e) {
    const overallTotal = document.getElementById("overall-total");
    const select = document.getElementById("select-shipping");
    let subTotal = document.getElementById("cart-subtotal").innerText;
    const selctedMethod = select.options[select.selectedIndex].value;
    if (selctedMethod) { 
        const response = await fetch(`/shop/api-shipping-details/${selctedMethod}/`);
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        const data =  await response.json();
        const shippingPrice = Number(data.price);
        subTotal = subTotal.replace(/,/g,"");
        subTotal = parseFloat(subTotal);
        const total = shippingPrice + subTotal;
        overallTotal.innerText = formatter.format(total);
    }else{
        overallTotal.innerText = subTotal;
    }
}
