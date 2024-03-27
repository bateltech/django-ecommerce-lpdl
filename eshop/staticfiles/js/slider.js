console.log("nique ta mère j'en ai marre");
const wrapper_details = document.querySelector(".wrapper_details");
const carousel_details = document.querySelector(".carousel_details");
const firstCardWidth = carousel_details.querySelector(".card_details").offsetWidth;
const arrowBtns = document.querySelectorAll(".wrapper_details i");
const carousel_detailsChildrens = [...carousel_details.children];
let isDragging = false, isAutoPlay = true, startX, startScrollLeft, timeoutId;
// Get the number of cards that can fit in the carousel_details at once
let cardPerView = Math.round(carousel_details.offsetWidth / firstCardWidth);
// Insert copies of the last few cards to beginning of carousel_details for infinite scrolling
carousel_detailsChildrens.slice(-cardPerView).reverse().forEach(card => {
    carousel_details.insertAdjacentHTML("afterbegin", card.outerHTML);
});
// Insert copies of the first few cards to end of carousel_details for infinite scrolling
carousel_detailsChildrens.slice(0, cardPerView).forEach(card => {
    carousel_details.insertAdjacentHTML("beforeend", card.outerHTML);
});
// Scroll the carousel_details at appropriate postition to hide first few duplicate cards on Firefox
carousel_details.classList.add("no-transition");
carousel_details.scrollLeft = carousel_details.offsetWidth;
carousel_details.classList.remove("no-transition");
// Add event listeners for the arrow buttons to scroll the carousel_details left and right
const swipingWidth = firstCardWidth + 25;
arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        carousel_details.scrollLeft += btn.id == "left" ? -swipingWidth : swipingWidth;
    });
});
const dragStart = (e) => {
    isDragging = true;
    carousel_details.classList.add("dragging");
    // Records the initial cursor and scroll position of the carousel_details
    startX = e.pageX;
    startScrollLeft = carousel_details.scrollLeft;
}
const dragging = (e) => {
    if(!isDragging) return; // if isDragging is false return from here
    // Updates the scroll position of the carousel_details based on the cursor movement
    carousel_details.scrollLeft = startScrollLeft - (e.pageX - startX);
}
const dragStop = () => {
    isDragging = false;
    carousel_details.classList.remove("dragging");
}
const infiniteScroll = () => {
    // If the carousel_details is at the beginning, scroll to the end
    if(carousel_details.scrollLeft === 0) {
        carousel_details.classList.add("no-transition");
        carousel_details.scrollLeft = carousel_details.scrollWidth - (2 * carousel_details.offsetWidth);
        carousel_details.classList.remove("no-transition");
    }
    // If the carousel_details is at the end, scroll to the beginning
    else if(Math.ceil(carousel_details.scrollLeft) === carousel_details.scrollWidth - carousel_details.offsetWidth) {
        carousel_details.classList.add("no-transition");
        carousel_details.scrollLeft = carousel_details.offsetWidth;
        carousel_details.classList.remove("no-transition");
    }
    // Clear existing timeout & start autoplay if mouse is not hovering over carousel_details
    clearTimeout(timeoutId);
    if(!wrapper_details.matches(":hover")) autoPlay();
}
const autoPlay = () => {
    if(window.innerWidth < 300 || !isAutoPlay) return; // Return if window is smaller than 800 or isAutoPlay is false
    // Autoplay the carousel_details after every 2000 ms
    timeoutId = setTimeout(() => carousel_details.scrollLeft += firstCardWidth, 2000);
}
autoPlay();
carousel_details.addEventListener("mousedown", dragStart);
carousel_details.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
carousel_details.addEventListener("scroll", infiniteScroll);
wrapper_details.addEventListener("mouseenter", () => clearTimeout(timeoutId));
wrapper_details.addEventListener("mouseleave", autoPlay);