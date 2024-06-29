console.log("ACCUEIL JS is running.");

/*============================= SLIDER NOUVEAUX ARTICLES =================================*/
let currentIndex = 0;
const slides = document.querySelectorAll('.slide_new');
const totalSlides = slides.length;
const sliderContainer = document.getElementById('slider-container-new');
let autoSlide;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove('active_new');
        if (i === index) {
            slide.classList.add('active_new');
        }
    });
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    showSlide(currentIndex);
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    showSlide(currentIndex);
}

function startAutoSlide() {
    autoSlide = setInterval(nextSlide, 5000);
}

function stopAutoSlide() {
    clearInterval(autoSlide);
}

document.getElementById('next').addEventListener('click', () => {
    stopAutoSlide();
    nextSlide();
    startAutoSlide();
});

document.getElementById('prev').addEventListener('click', () => {
    stopAutoSlide();
    prevSlide();
    startAutoSlide();
});

// Pause the slider when the mouse is over the slider container
sliderContainer.addEventListener('mouseover', stopAutoSlide);

// Resume the slider when the mouse leaves the slider container
sliderContainer.addEventListener('mouseout', startAutoSlide);

showSlide(currentIndex);
startAutoSlide();