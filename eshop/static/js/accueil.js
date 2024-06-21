/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')
    
const scrollActive = () =>{
  	const scrollY = window.pageYOffset

	sections.forEach(current =>{
		const sectionHeight = current.offsetHeight,
			  sectionTop = current.offsetTop - 58,
			  sectionId = current.getAttribute('id'),
			  sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')

		if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
			sectionsClass.classList.add('active-link')
		}else{
			sectionsClass.classList.remove('active-link')
		}                                                    
	})
}
window.addEventListener('scroll', scrollActive)

/*=============== SHOW SCROLL UP ===============*/ 
const scrollUp = () =>{
	const scrollUp = document.getElementById('scroll-up')
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the a tag with the scrollup class
	this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
						: scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    this.scrollY >= 230 ? header.classList.add('bg-header') 
                       : header.classList.remove('bg-header')
}
window.addEventListener('scroll', scrollHeader)

const scrollNav = () => {
    const header = document.getElementById('nav-bar');
    const main = document.querySelector('.main');

    if (window.scrollY >= 240) {
        header.classList.add('fixed_nav');
        main.style.paddingTop = '4rem';
    } else {
        header.classList.remove('fixed_nav');
        main.style.paddingTop = '0';
    }
}

window.addEventListener('scroll', scrollNav)

/* Barre de recherche */
let searchIcons = document.querySelectorAll('.search__icon');

searchIcons.forEach(function(icon) {
  icon.addEventListener('click', function() {
    let searchBar = document.getElementById('searchBar');
    searchBar.style.width == '20%' ? searchBar.style.width = '0' : searchBar.style.width = '20%';
    let searchBarMobile = document.getElementById('searchBarMobile');
    searchBarMobile.style.width == '80%' ? searchBarMobile.style.width = '0' : searchBarMobile.style.width = '90%';
  });
});

window.addEventListener('scroll', function () {
    document.getElementById('searchBar').style.width = '0';
    document.getElementById('searchBarMobile').style.width = '0';
});

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


/*============================= SLIDER NOUVEAUX ARTICLES =================================*/
document.addEventListener('DOMContentLoaded', function() {
    var popup = document.getElementById('sales-popup');
    var closeBtn = document.querySelector('.close-modal-btn');

    // Show the popup
    popup.style.display = 'block';

    // Close the popup when the close button is clicked
    closeBtn.addEventListener('click', function() {
        popup.style.display = 'none';
    });
});
