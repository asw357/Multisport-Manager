// Voorbereiding voor taalondersteuning
const translations = {
  nl: {
    welcome: "Welkom bij de Sport Manager Simulatie",
    news: "Laatste Nieuws",
  },
  en: {
    welcome: "Welcome to the Sport Manager Simulation",
    news: "Latest News",
  },
  fr: {
    welcome: "Bienvenue dans la simulation de gestion sportive",
    news: "Dernières nouvelles",
  },
  de: {
    welcome: "Willkommen bei der Sportmanager-Simulation",
    news: "Neueste Nachrichten",
  },
};

function getUserLanguage() {
  const lang = navigator.language || navigator.userLanguage;
  return lang.slice(0, 2); // bijvoorbeeld "nl" van "nl-NL"
}

function applyLanguage() {
  const lang = getUserLanguage();
  const t = translations[lang] || translations['en'];

  const header = document.querySelector('header h1');
  const newsSection = document.querySelector('#news-headlines h2');

  if (header) header.textContent = t.welcome;
  if (newsSection) newsSection.textContent = t.news;
}

document.addEventListener('DOMContentLoaded', applyLanguage);
