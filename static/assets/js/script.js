// const logregBox=document.querySelector('.logreg-box');
// const loginLink=document.querySelector('.login-link');
// const registerLink=document.querySelector('.register-link');

// loginLink.addEventListener('click',()=>{
//   logregBox.classList.add('active');
// });
// registerLink.addEventListener('click',()=>{
//   logregBox.classList.remove('active');
// });

// SHOW MENU

const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.add('show-menu')
  })
}
/*===== MENU HIDE =====*/
/* Validate if constant exists */
if(navClose) {
  navClose.addEventListener('click', () => {
    navMenu.classList.remove('show-menu')
  })
}
/*===== REMOVE MENU MOBILE =====*/
const navLink=document.querySelectorAll('.nav_link')
const linkAction = () => {
  const navMenu = document.getElementById('nav-menu')
  // When we click on each nav_link, we remove the show-menu class
  navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*===== ABB BLUR TO HEADER =====*/
const blurHeader = () =>{
  const header = document.getElementById('header')
  // When the scroll is greater than 50 viewport height, add the blur-header class to the header tag
  this.scrollY >= 50? header.classList.add('blur-header')
                    : header.classList.remove('blur-header')
  }
  window.addEventListener('scroll', blurHeader)


/*===== ACTIVE LINK =====*/
const sections=document.querySelectorAll('section[id]')
const scrollActive = () => {
  const scrollY=window.scrollY;
  
  sections.forEach(current =>{
    const sectionHeight=current.offsetHeight,
          sectionTop=current.offsetTop-58,
          sectionId=current.getAttribute('id'),
          sectionsClass=document.querySelector('.nav_menu a[href*=' + sectionId+ ']');

    if (scrollY>sectionTop && scrollY<=sectionTop+sectionHeight){
      sectionsClass.classList.add('active-link')
    }
    else{
      sectionsClass.classList.remove('active-link')
    }
  })
}
window.addEventListener('scroll',scrollActive)


/*===== SCROLL REVEAL =====*/
const sr=ScrollReveal({
  origin:'top',
  distance: '60px',
  duration:3000,
  delay: 400,

})

sr.reveal('.home_data,.footer_container');
sr.reveal('.home_card',{delay:500,distance:'100px',interval:100});
sr.reveal('.about_data',{origin:'right'});
sr.reveal('.about_img',{origin:'left'});

/*===== MENU HIDE =====*/