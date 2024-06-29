
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

        if (sectionsClass) {
            if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
                sectionsClass.classList.add('active-link')
            }else{
                sectionsClass.classList.remove('active-link')
            } 
        }                                                  
	})
}
window.addEventListener('scroll', scrollActive)


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

/* HORIZONTAL SCROLL BAR FOR CATEGORY FILTERS ON MOBILE */

// JavaScript to enable click-and-drag scrolling
const scrollContainerMob = document.getElementById('scroll-container');

// Vérifiez si scrollContainerMob n'est pas nul
if (scrollContainerMob) {
    let isDragging = false;
    let startX, scrollLeft;

    scrollContainerMob.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX - scrollContainerMob.offsetLeft;
        scrollLeft = scrollContainerMob.scrollLeft;
        scrollContainerMob.style.cursor = 'grabbing'; // Change cursor style when dragging
    });

    scrollContainerMob.addEventListener('mouseleave', () => {
        isDragging = false;
        scrollContainerMob.style.cursor = 'grab'; // Restore cursor style when not dragging
    });

    scrollContainerMob.addEventListener('mouseup', () => {
        isDragging = false;
        scrollContainerMob.style.cursor = 'grab'; // Restore cursor style when not dragging
    });

    scrollContainerMob.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - scrollContainerMob.offsetLeft;
        const walk = (x - startX) * 2; // Adjust the scrolling speed if needed
        scrollContainerMob.scrollLeft = scrollLeft - walk;
    });
}

/* ####################################### */
/* ########## Fonctions Backend ########## */
/* ####################################### */

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript MAIN is running."); // Vérifiez si ce message s'affiche dans la console.
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const errorMessage = document.getElementById("error-message");
    
    const signupForm = document.querySelector(".login__form");
    if(signupForm){
        signupForm.addEventListener("submit", function (event) {
            if (passwordInput.value !== confirmPasswordInput.value) {
                event.preventDefault(); // Empêche l'envoi du formulaire et la recharge de la page
                errorMessage.textContent = "Les mots de passe ne correspondent pas";
                errorMessage.style.display = "block"; // Rendre la div visible
            }
        });
    }
    else{
        console.log("signupForm élément introuvable sur cette page.");
    }

});

/*-----------------------------------*\
* ARTICLES.HTML
\*-----------------------------------*/

document.addEventListener('DOMContentLoaded', function() {
    console.log("ARTICLES javascript is running");
    const categoryLinks = document.querySelectorAll('.category');
    const subcategoryButtons = document.querySelectorAll('.rounded-button');
    const productCards = document.querySelectorAll('.product-card');

    // Function to filter product cards based on subcategory ID
    function filterProductCards(subcategoryId) {
        productCards.forEach(card => {
            console.log("inside product card loop");
            const articleSubcategory = card.getAttribute('article-sub-category');
            if (articleSubcategory === subcategoryId || subcategoryId === 'all') {
                card.style.display = 'grid';
            } else {
                card.style.display = 'none';
            }
        });
    }

    function filterProductCardsByCategory(categoryId) {
        productCards.forEach(card => {
            const articleCategory = card.getAttribute('article-category');
            if (articleCategory === categoryId || categoryId === 'all') {
                card.style.display = 'grid';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Event listener for category links
    categoryLinks.forEach(link => {
        console.log("inside category links loop");
        link.addEventListener('click', function(event) {
            console.log("link clicked");
            event.preventDefault();
            const categoryId = this.getAttribute('category-id');
            // Remove 'active' class from all category links
            categoryLinks.forEach(link => {
                link.classList.remove('active');
            });

            // Add 'active' class to the clicked category link
            this.classList.add('active');

            filterProductCardsByCategory(categoryId);
            subcategoryButtons.forEach(btn => {
                btn.classList.remove('clicked');
            });

            // Update the selected category text
            const selectedCategoryText = document.getElementById('selected-category');
            const selectedCategoryTitle = document.getElementById('title-category');
            const selectedSubCategoryText = document.getElementById('selected-subcategory');
            selectedCategoryText.textContent = " / " + categoryId;
            selectedCategoryTitle.textContent = categoryId;
            selectedSubCategoryText.textContent = "";

            // Hide all subcategory buttons
            subcategoryButtons.forEach(button => {
                console.log("inside sub category loop");
                const subcategoryId = button.getAttribute('sub-category-id');
                console.log("subcategory id : ", subcategoryId);
                console.log("category id : ", categoryId);
                if (subcategoryId.startsWith(categoryId)) {
                    button.style.display = 'inline-block';
                } else {
                    button.style.display = 'none';
                }
            });

            // Filter and hide articles of the previous category
            productCards.forEach(card => {
                console.log("inside product card loop not function");
                const articlecategory = card.getAttribute('article-category');
                console.log(" WOOHOO articlecategory id : ", articlecategory);
                console.log(" WOOHOO category id : ", categoryId);
                if (!articlecategory.startsWith(categoryId)) {
                    card.style.display = 'none';
                }
            });

        });
        
    });

    // Select all category buttons
    const categoryButtons = document.querySelectorAll('.category-button');

    // Event listener for category buttons
    categoryButtons.forEach(button => {
        console.log("inside category buttons loop");
        button.addEventListener('click', function(event) {
            console.log("button clicked");
            event.preventDefault();
            const categoryId = this.getAttribute('mob-category-id');
            // Remove 'clicked' class from all category buttons
            categoryButtons.forEach(button => {
                button.classList.remove('clicked');
            });

            // Add 'clicked' class to the clicked category button
            this.classList.add('clicked');

            filterProductCardsByCategory(categoryId);
            subcategoryButtons.forEach(btn => {
                btn.classList.remove('clicked');
            });

            // Update the selected category text
            const selectedCategoryText = document.getElementById('selected-category');
            const selectedCategoryTitle = document.getElementById('title-category');
            const selectedSubCategoryText = document.getElementById('selected-subcategory');
            selectedCategoryText.textContent = " / " + categoryId;
            selectedCategoryTitle.textContent = categoryId;
            selectedSubCategoryText.textContent = "";

            // Hide all subcategory buttons
            subcategoryButtons.forEach(button => {
                console.log("inside sub category loop");
                const subcategoryId = button.getAttribute('sub-category-id');
                console.log("subcategory id : ", subcategoryId);
                console.log("category id : ", categoryId);
                if (subcategoryId.startsWith(categoryId)) {
                    button.style.display = 'inline-block';
                } else {
                    button.style.display = 'none';
                }
            });

            // Filter and hide articles of the previous category
            productCards.forEach(card => {
                console.log("inside product card loop not function");
                const articlecategory = card.getAttribute('article-category');
                console.log(" WOOHOO articlecategory id : ", articlecategory);
                console.log(" WOOHOO category id : ", categoryId);
                if (!articlecategory.startsWith(categoryId)) {
                    card.style.display = 'none';
                }
            });

        });
    });

    

    // Event listener for subcategory buttons
    subcategoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log("sub category button clicked");
            // Remove 'clicked' class from all buttons
            subcategoryButtons.forEach(btn => {
                btn.classList.remove('clicked');
            });
            // Add 'clicked' class to the clicked button
            this.classList.add('clicked');
            const subcategoryarticleId = this.getAttribute('sub-category-article-id');

            const selectedSubCategoryText = document.getElementById('selected-subcategory');
            selectedSubCategoryText.textContent = " / " + this.getAttribute('sub-category-libelle');
            filterProductCards(subcategoryarticleId);
        });
    });

    // Get the heart icon container
    const heartIcons = document.querySelectorAll('.heart-icon');
    
    // Trigger click event on the heart icon is clicked
    heartIcons.forEach(icon => {
        icon.addEventListener('click', function(){
            console.log("heart clicked");
            const outlineHeart = this.querySelector('.heart-outline');
            const redHeart = this.querySelector('.heart-red');
            outlineHeart.classList.toggle('hidden');
            redHeart.classList.toggle('hidden');
            
            // add to favorite code.
        });
    });
});

/*-----------------------------------*\
* ACCUEIL.HTML
\*-----------------------------------*/
/*============================= PROMO POPUP =================================*/
document.addEventListener('DOMContentLoaded', function() {
    var popup = document.getElementById('sales-popup');
    var closeBtn = document.querySelector('.close-modal-btn');

    console.log('promo popup js');

    if(popup){
        // Show the popup
        popup.style.display = 'block';
    }

    if(closeBtn){
        // Close the popup when the close button is clicked
        closeBtn.addEventListener('click', function() {
            popup.style.display = 'none';
        });
    }
});

/* ###################################### */
/* ######## end of DOM functions ######## */
/* ###################################### */


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
