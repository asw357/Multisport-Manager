const translations = {
  nl: {
    "welcome-title": "Welkom bij Multisport-Manager",
    "welcome-text": "Beheer je eigen nationale team in een fictieve Olympische wereld.",
    "register-button": "Registreren",
    "login-button": "Inloggen"
  },
  en: {
    "welcome-title": "Welcome to Multisport-Manager",
    "welcome-text": "Manage your own national team in a fictional Olympic world.",
    "register-button": "Register",
    "login-button": "Login"
  },
  fr: {
    "welcome-title": "Bienvenue sur Multisport-Manager",
    "welcome-text": "Gérez votre propre équipe nationale dans un monde olympique fictif.",
    "register-button": "S'inscrire",
    "login-button": "Connexion"
  },
  de: {
    "welcome-title": "Willkommen bei Multisport-Manager",
    "welcome-text": "Verwalte dein eigenes Nationalteam in einer fiktiven olympischen Welt.",
    "register-button": "Registrieren",
    "login-button": "Anmelden"
  }
};

const switcher = document.getElementById('language-switcher');

function updateTexts(lang) {
  const elements = document.querySelectorAll('[id]');
  elements.forEach(el => {
    if (translations[lang] && translations[lang][el.id]) {
      el.innerText = translations[lang][el.id];
    }
  });
}

switcher.addEventListener('change', (e) => {
  const lang = e.target.value;
  updateTexts(lang);
});

window.addEventListener('DOMContentLoaded', () => {
  updateTexts('nl');
});
