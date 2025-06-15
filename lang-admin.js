const translations = {
  nl: {
    "admin-title": "Adminpaneel",
    "admin-section-title": "Beheeropties",
    "edit-editions": "Beheer Edities",
    "edit-events": "Beheer Onderdelen",
    "edit-athletes": "Beheer Atleten",
    "edit-countries": "Beheer Landen",
    "simulate-day": "Simuleer Volgende Dag"
  },
  en: {
    "admin-title": "Admin Panel",
    "admin-section-title": "Management Options",
    "edit-editions": "Manage Editions",
    "edit-events": "Manage Events",
    "edit-athletes": "Manage Athletes",
    "edit-countries": "Manage Countries",
    "simulate-day": "Simulate Next Day"
  },
  fr: {
    "admin-title": "Panneau d'administration",
    "admin-section-title": "Options de gestion",
    "edit-editions": "Gérer les éditions",
    "edit-events": "Gérer les épreuves",
    "edit-athletes": "Gérer les athlètes",
    "edit-countries": "Gérer les pays",
    "simulate-day": "Simuler le jour suivant"
  },
  de: {
    "admin-title": "Admin-Bereich",
    "admin-section-title": "Verwaltungsoptionen",
    "edit-editions": "Editionen verwalten",
    "edit-events": "Wettbewerbe verwalten",
    "edit-athletes": "Athleten verwalten",
    "edit-countries": "Länder verwalten",
    "simulate-day": "Nächsten Tag simulieren"
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
