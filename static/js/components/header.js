// ? GETTING DOC ELEMENTS
const themeControl = document.getElementById("theme-control");
const menuBtns = document.querySelectorAll(".menu-btn");
const navbar = document.querySelector(".nav");

// * FUNCTION TO SAVE THEME PREFERENCE
function saveThemePreference(theme) {
    localStorage.setItem('theme', theme);
}

// * FUNCTION TO LOAD THEME PREFERENCE
function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme');
    document.body.classList.toggle('dark', savedTheme === 'dark');
}

// * FUNCTION TO TOGGLE THEME
function toggleTheme() {
    if (document.body.classList.contains('dark')) {
        document.body.classList.remove('dark');
    } else {
        document.body.classList.add('dark');
    }

    saveThemePreference(document.body.classList.contains('dark') ? 'dark' : 'light');
}

// * FUNCTION TO TOGGLE NAVBAR
function toggleNav() {
    if (navbar.classList.contains('show')) {
        navbar.classList.remove('show');

        setTimeout(() => {
            navbar.style.display = 'none';
        }, 500);
    } else {
        navbar.style.display = 'flex';

        setTimeout(() => {
            navbar.classList.add('show');
        }, 100);
    }
}

// & EVENT LISTENER FOR THEME TOGGLE
themeControl.addEventListener('click', toggleTheme);
loadThemePreference();

// & EVENT LISTENER FOR NAVBAR TOGGLE
menuBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        toggleNav();
    });
});