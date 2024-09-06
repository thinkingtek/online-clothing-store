const modalBox = document.getElementById("modal-overlay");
const deleteItemModal = document.getElementById("delete-item-modal");
const clearCartModal = document.getElementById("clear-cart-modal");
const body = document.getElementById("body-id");

// Close modal
function closeModal() {
    modalBox.style.display = "none";
    body.classList.remove("body-overflow-hidden")
    deleteItemModal ? deleteItemModal.style.display = "none": "" ;
    clearCartModal ? clearCartModal.style.display = "none": "" ;
}

// Show clear cart modal
function showClearModal() {
    deleteItemModal ? deleteItemModal.style.display = "none": "" ;
    body.classList.add("body-overflow-hidden")
    modalBox.style.display = "flex";
    clearCartModal.style.display = "block";
}

// show delete cart item modal and set the href(link) attribute to the specific cart item to be deleted
function showDeleteModal(e) {
    e.stopPropagation();
    clearCartModal ? clearCartModal.style.display = "none": "" ;
    body.classList.add("body-overflow-hidden");
    modalBox.style.display = "flex";
    deleteItemModal.style.display = "block";
    const modalHref = document.getElementById("cart-item-href");
    const link = e.target.getAttribute('data-name');
    modalHref.setAttribute("href",link);
}