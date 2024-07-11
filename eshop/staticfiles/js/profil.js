/* sidebar menu for profil.html */
console.log("profil js is running.");

function openNav() {
    document.getElementsByClassName("sidebar")[0].style.width = "250px";
    document.getElementsByClassName("side-openbtn")[0].style.display = "none";
  }
  
function closeNav() {
    document.getElementsByClassName("sidebar")[0].style.width = "0";
    document.getElementsByClassName("side-openbtn")[0].style.display = "inline";
  }
