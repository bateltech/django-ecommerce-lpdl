console.log("ACCUEIL JS is running.");

/*============================= SLIDER NOUVEAUX ARTICLES =================================*/
let currentIndex = 0;
const slides = document.querySelectorAll('.slide_new');
const totalSlides = slides.length;
const sliderContainer = document.getElementById('slider-container-new');
let autoSlide;
let slideTimeout;

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

function resetAutoSlide() {
    clearTimeout(slideTimeout);
    stopAutoSlide(); // Arrête l'autoslide existant
    slideTimeout = setTimeout(startAutoSlide, 5000); // Relance l'autoslide après l'intervalle complet
}

document.getElementById('next').addEventListener('click', () => {
    nextSlide();
    resetAutoSlide();
});

document.getElementById('prev').addEventListener('click', () => {
    prevSlide();
    resetAutoSlide();
});

// Pause the slider when the mouse is over the slider container
sliderContainer.addEventListener('mouseover', stopAutoSlide);

// Resume the slider when the mouse leaves the slider container
sliderContainer.addEventListener('mouseout', (event) => {
    // Vérifie si le curseur est toujours dans le slider container
    if (!sliderContainer.contains(event.relatedTarget)) {
        resetAutoSlide();
    }
});

showSlide(currentIndex);  // Affiche la première slide immédiatement
startAutoSlide();         // Démarre l'autoslide dès le début
