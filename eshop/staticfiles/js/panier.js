/* =========================PANIER.html SCRIPTS ====================================*/
function changeCounter(itemId, value) {
    console.log('Updating quantity for itemId:', itemId);
    const counterElement = document.getElementById(`counter${itemId}`);
    const newQuantity = parseInt(counterElement.textContent) + value;

    if (newQuantity > 0) {
        // Update the counter value in the DOM
        counterElement.textContent = newQuantity;

        // Send AJAX request to update the quantity on the server
        updateQuantityOnServer(itemId, newQuantity);
    }
}

function updateMobileCounter(itemId, newQuantity) {
    const mobileCounterElement = document.querySelector(`.button-item-mobile [id="counter${itemId}"]`);
    if (mobileCounterElement) {
        mobileCounterElement.textContent = newQuantity;
    }
}

function updateQuantityOnServer(itemId, newQuantity) {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log('Updating quantity for itemId:', itemId);

    console.log('Updating quantity on the server...');

    fetch(`/update_quantity_ajax/${itemId}/${newQuantity}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Quantity updated successfully:', data);
        updateItemPrice(itemId);
        updateMobileCounter(itemId, newQuantity);
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
    });
}

function updateItemPrice(itemId) {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(`/get_item_price/${itemId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Update item price and total price in HTML dynamically
        const itemPriceElement = document.getElementById(`itemPrice_${itemId}`);
        const seconditemPriceElement = document.getElementById(`seconditemPrice_${itemId}`);
        const totalPriceElement = document.getElementById('totalPriceElement');

        // Update the item price
        itemPriceElement.textContent = data.item_price +" €";
        seconditemPriceElement.textContent = data.total_item_price +" €";

        const mobileItemPriceElement = document.querySelector(`.taille-prix-mobile [id="itemPrice_${itemId}"]`);
        if (mobileItemPriceElement) {
            mobileItemPriceElement.textContent = data.item_price +" €";
        }

        // Update the total price
        totalPriceElement.textContent = data.total_price +" €";

        console.log('Item price updated successfully:', data.item_price);
        console.log('Total price updated successfully:', data.total_price);
    })
    .catch(error => {
        console.error('Error updating item price:', error);
    });
}

function deleteCartItem(itemId) {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(`/delete_Cart_item_ajax/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Supprimer', data);

        // Supprimer l'élément de la section panier_section
        const itemElement = document.getElementById(`cartItem${itemId}`);
        if (itemElement) {
            itemElement.remove();
        }

        // Supprimer l'élément de la section section_total
        // const itemTotalElement = document.getElementById(`cartItemTotal${itemId}`);
        const itemTotalElement = document.querySelector(`.cart_item[data-item-id="${itemId}"]`);

        if (itemTotalElement) {
            itemTotalElement.remove();
        }

        // Mettre à jour le prix total
        const totalPriceElement = document.getElementById('totalPriceElement');
        const currentTotalPrice = parseFloat(totalPriceElement.textContent.replace(' €', ''));
        const itemPrice = parseFloat(data.total_item_price);
        const newTotalPrice = currentTotalPrice - itemPrice;
        totalPriceElement.textContent = newTotalPrice.toFixed(2) + ' €';
    })
    .catch(error => {
        console.error('Error supp item:', error);
    });
}

function openForm() {
    document.getElementById("popupOverlay").style.display = "flex";
    console.log('Opening the form');
}

function closeForm() {
    document.getElementById("popupOverlay").style.display = "none";
    console.log('Closing the form');

}

function submitFeedback() {
    const form = document.getElementById('feedbackForm');
    form.submit();  // This will submit the form using the traditional approach
}