// Dummy headlines (worden later vervangen door dynamische data)
const dummyHeadlines = [
  "🏅 Goud voor Duitsland op de 100m sprint!",
  "🔥 Nieuw Multi Record bij het schansspringen!",
  "🇫🇷 Frankrijk leidt na dag 3 van de Zomereditie",
  "🚨 Blessure voor topfavoriet in zwemmen",
  "🥇 IJsland pakt verrassend goud in touwtrekken"
];

function loadHeadlines() {
  const list = document.getElementById('headlines');
  if (!list) return;

  dummyHeadlines.forEach((headline) => {
    const li = document.createElement('li');
    li.textContent = headline;
    list.appendChild(li);
  });
}

document.addEventListener('DOMContentLoaded', loadHeadlines);
