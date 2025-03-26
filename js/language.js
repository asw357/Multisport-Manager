const translations = {
  nl: {
    welkom: "Welkom bij Sport Manager Simulatie",
    registreren: "Registreren",
    inloggen: "Inloggen",
    uitloggen: "Uitloggen",
    manager: "Managerpagina",
    nieuws: "Laatste Nieuws",
    volgende: "Volgende Live Wedstrijd",
    intro: "Stap in de rol van manager van jouw nationale team en leid jouw land naar glorie! Stel atleten op, scout nieuw talent, pas tactieken toe en win medailles! Lees ook de Regels & Uitleg voordat je begint."
  },
  en: {
    welkom: "Welcome to Sport Manager Simulation",
    registreren: "Register",
    inloggen: "Login",
    uitloggen: "Logout",
    manager: "Manager Page",
    nieuws: "Latest News",
    volgende: "Next Live Match",
    intro: "Step into the role of a national team manager and lead your country to glory! Select athletes, scout new talent, set tactics and win medals! Also read the Rules & Explanation before starting."
  },
  de: {
    welkom: "Willkommen bei Sport Manager Simulation",
    registreren: "Registrieren",
    inloggen: "Anmelden",
    uitloggen: "Abmelden",
    manager: "Managerseite",
    nieuws: "Neueste Nachrichten",
    volgende: "Nächstes Live-Match",
    intro: "Übernimm die Rolle eines Nationaltrainers und führe dein Land zum Ruhm! Wähle Athleten, scoute Talente, setze Taktiken ein und gewinne Medaillen! Lies auch die Regeln & Erklärungen vor dem Start."
  },
  fr: {
    welkom: "Bienvenue dans la Simulation de Sport Manager",
    registreren: "S'inscrire",
    inloggen: "Connexion",
    uitloggen: "Déconnexion",
    manager: "Page du Manager",
    nieuws: "Dernières Nouvelles",
    volgende: "Prochain Match en Direct",
    intro: "Prenez le rôle d’un entraîneur national et menez votre pays à la gloire ! Sélectionnez des athlètes, recrutez des talents, définissez des tactiques et gagnez des médailles ! Consultez aussi les Règles & Explications avant de commencer."
  }
};

function translatePage(taal) {
  const vertalingen = translations[taal] || translations.nl;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const sleutel = el.getAttribute("data-i18n");
    if (vertalingen[sleutel]) {
      el.textContent = vertalingen[sleutel];
    }
  });
}
