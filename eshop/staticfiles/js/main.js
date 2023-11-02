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



/*const sections = document.querySelectorAll('section[id]')
    
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
*/



// Select all navigation links with anchor hrefs
const navLinks = document.querySelectorAll('.anchor__link');

// Add click event listener to each navigation link
navLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default link behavior

        const targetId = link.getAttribute('href'); // Get the target anchor ID
        const targetElement = document.querySelector(targetId); // Find the target element

        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth', // Use smooth scrolling
            });
        }
    });
});


// /*=============== SHOW SCROLL UP ===============*/ 
// const scrollUp = () =>{
// 	const scrollUp = document.getElementById('scroll-up')
//     // When the scroll is higher than 350 viewport height, add the show-scroll class to the a tag with the scrollup class
// 	this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
// 						: scrollUp.classList.remove('show-scroll')
// }
// window.addEventListener('scroll', scrollUp)

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    this.scrollY >= 50 ? header.classList.add('bg-header') 
                       : header.classList.remove('bg-header')
}
window.addEventListener('scroll', scrollHeader)


/* HORIZONTAL SCROLL BAR FOR FILTERS */

// JavaScript to enable click-and-drag scrolling
const scrollContainer = document.getElementById('scrollContainer');

// Vérifiez si scrollContainer n'est pas nul
if (scrollContainer) {
    let isDragging = false;
    let startX, scrollLeft;

    scrollContainer.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX - scrollContainer.offsetLeft;
        scrollLeft = scrollContainer.scrollLeft;
        scrollContainer.style.cursor = 'grabbing'; // Change cursor style when dragging
    });

    scrollContainer.addEventListener('mouseleave', () => {
        isDragging = false;
        scrollContainer.style.cursor = 'grab'; // Restore cursor style when not dragging
    });

    scrollContainer.addEventListener('mouseup', () => {
        isDragging = false;
        scrollContainer.style.cursor = 'grab'; // Restore cursor style when not dragging
    });

    scrollContainer.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - scrollContainer.offsetLeft;
        const walk = (x - startX) * 2; // Adjust the scrolling speed if needed
        scrollContainer.scrollLeft = scrollLeft - walk;
    });
}


/* ####################################### */
/* ########## Fonctions Backend ########## */
/* ####################################### */

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is running."); // Vérifiez si ce message s'affiche dans la console.
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const errorMessage = document.getElementById("error-message");
    
    const signupForm = document.querySelector(".login__form");
    signupForm.addEventListener("submit", function (event) {
        if (passwordInput.value !== confirmPasswordInput.value) {
            event.preventDefault(); // Empêche l'envoi du formulaire et la recharge de la page
            errorMessage.textContent = "Les mots de passe ne correspondent pas";
            errorMessage.style.display = "block"; // Rendre la div visible
        }
    });
});

