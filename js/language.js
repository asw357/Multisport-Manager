const vertalingen = {
  nl: {
    title: "Multisport-Manager",
    heading: "🏅 Multisport-Manager",
    login: "🔐 Inloggen",
    register: "🆕 Registreren",
    welcome-title: "🌍 Welkom bij de Multisport-Manager",
    welcome-text: "Leid jouw land naar internationale sportglorie in deze realistische en meeslepende multiplayer-managementgame. Ontdek tientallen sporten, stel je team samen, en strijd tegen managers over de hele wereld. 📅 Toernooien spelen zich af in real-time — net als in het echt!",
    read-rules: "📖 Lees de spelregels en uitleg",
    news: "📰 Laatste nieuws",
    news1: "🎉 Eerste editie is in voorbereiding...",
    news2: "📢 Registreer nu en ontvang start-MP!",
    news3: "⚙️ Admins werken hard aan nieuwe simulatie-opties.",
    countries: "🌐 Deelnemende landen",
    no-countries: "Er zijn nog geen landen toegewezen.",
    footer: "&copy; 2025 Multisport-Manager – Jouw sport, jouw strategie."
  },
  en: {
    title: "Multisport Manager",
    heading: "🏅 Multisport Manager",
    login: "🔐 Log In",
    register: "🆕 Sign Up",
    welcome-title: "🌍 Welcome to Multisport Manager",
    welcome-text: "Lead your nation to international sports glory in this realistic and immersive multiplayer management game. Discover dozens of sports, build your team, and compete with managers around the world. 📅 Tournaments take place in real-time — just like in real life!",
    read-rules: "📖 Read the rules and explanation",
    news: "📰 Latest news",
    news1: "🎉 First edition is coming soon...",
    news2: "📢 Register now and receive starting MP!",
    news3: "⚙️ Admins are working hard on new simulation features.",
    countries: "🌐 Participating countries",
    no-countries: "No countries assigned yet.",
    footer: "&copy; 2025 Multisport Manager – Your sport, your strategy."
  },
  fr: {
    title: "Multisport-Manager",
    heading: "🏅 Multisport-Manager",
    login: "🔐 Connexion",
    register: "🆕 Inscription",
    welcome-title: "🌍 Bienvenue sur Multisport-Manager",
    welcome-text: "Menez votre nation à la gloire sportive dans ce jeu de gestion multijoueur réaliste et immersif. Découvrez des dizaines de sports, construisez votre équipe et affrontez des managers du monde entier. 📅 Les tournois se déroulent en temps réel — comme dans la réalité !",
    read-rules: "📖 Lire les règles et explications",
    news: "📰 Dernières nouvelles",
    news1: "🎉 La première édition est en préparation...",
    news2: "📢 Inscrivez-vous maintenant et recevez des MP de départ !",
    news3: "⚙️ Les administrateurs travaillent sur de nouvelles fonctions.",
    countries: "🌐 Pays participants",
    no-countries: "Aucun pays encore attribué.",
    footer: "&copy; 2025 Multisport-Manager – Votre sport, votre stratégie."
  },
  de: {
    title: "Multisport-Manager",
    heading: "🏅 Multisport-Manager",
    login: "🔐 Anmelden",
    register: "🆕 Registrieren",
    welcome-title: "🌍 Willkommen bei Multisport-Manager",
    welcome-text: "Führe dein Land zum sportlichen Ruhm in diesem realistischen und fesselnden Multiplayer-Managementspiel. Entdecke Dutzende Sportarten, stelle dein Team zusammen und konkurriere mit Managern weltweit. 📅 Turniere finden in Echtzeit statt – wie in der Realität!",
    read-rules: "📖 Spielregeln und Erklärung lesen",
    news: "📰 Neueste Nachrichten",
    news1: "🎉 Erste Ausgabe in Vorbereitung...",
    news2: "📢 Jetzt registrieren und Start-MP sichern!",
    news3: "⚙️ Admins arbeiten an neuen Simulationsfunktionen.",
    countries: "🌐 Teilnehmende Länder",
    no-countries: "Noch keine Länder zugewiesen.",
    footer: "&copy; 2025 Multisport-Manager – Dein Sport, deine Strategie."
  }
};

function vertaalPagina() {
  const taal = localStorage.getItem("taal") || "nl";
  document.querySelectorAll("[data-i18n]").forEach(elem => {
    const key = elem.getAttribute("data-i18n");
    if (vertalingen[taal] && vertalingen[taal][key]) {
      elem.innerHTML = vertalingen[taal][key];
    }
  });
}
